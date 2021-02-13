import subprocess
import time
from multiprocessing import Event
from multiprocessing.synchronize import Event as EventClass
from queue import Queue, Empty
from threading import Thread

from .base import wait_and_measure_thread, process_kill_thread, preexec_fn_merge
from ..model import ProcessResult
from ...utils import args_split


class InteractiveProcess:
    def __init__(self, process: subprocess.Popen, start_time: float,
                 output_yield_func, result_func, lifetime_event: EventClass):
        self.__process = process
        self.__start_time = start_time
        self.__output_yield = output_yield_func()
        self.__result_func = result_func
        self.__lifetime_event = lifetime_event

    @property
    def result(self) -> ProcessResult:
        return self.__result_func()

    @property
    def start_time(self) -> float:
        return self.__start_time

    @property
    def output_yield(self):
        return self.__output_yield

    def print_stdin(self, *args, **kwargs):
        kwargs['file'] = self.__process.stdin
        kwargs['flush'] = kwargs.get('flush', True)
        print(*args, **kwargs)

    def close_stdin(self):
        self.__process.stdin.close()

    def join(self):
        return self.__lifetime_event.wait()


def _read_stream(stream, start_time: float, tag: str, queue: Queue):
    _line_queue = Queue()
    _queue_complete = Event()

    def _monitor_func():
        for _line in stream:
            _line_queue.put((time.time() - start_time, _line))

        _queue_complete.set()

    def _output_func():
        while not _line_queue.empty() or not _queue_complete.is_set():
            try:
                _time, _line = _line_queue.get(timeout=0.2)
            except Empty:
                pass
            else:
                _line = _line.rstrip('\r\n')
                queue.put((_time, tag, _line))

    _monitor_thread = Thread(target=_monitor_func)
    _output_thread = Thread(target=_output_func)

    _monitor_thread.start()
    _output_thread.start()

    _monitor_thread.join()
    _output_thread.join()


def interactive_process(args, preexec_fn=None, real_time_limit=None) -> InteractiveProcess:
    _full_lifetime_complete = Event()
    _start_time_ok, _start_time, _before_exec = preexec_fn_merge(preexec_fn)

    process = subprocess.Popen(
        args=args_split(args),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=1,
        universal_newlines=True,
        preexec_fn=_before_exec,
    )

    # thread for process control and resource measure
    resource_measure_thread, _process_complete, _process_result = \
        wait_and_measure_thread(_start_time_ok, _start_time, process)
    resource_measure_thread.start()

    # thread for killing the process when real time exceed
    killer_thread = process_kill_thread(_start_time_ok, _start_time, process, real_time_limit, _process_complete)
    killer_thread.start()

    # output control thread
    _all_output_queue = Queue()
    _all_output_start = Event()
    _all_output_complete = Event()
    _start_time_ok.wait()
    stdout_thread = Thread(target=lambda: _read_stream(process.stdout, _start_time.value, 'stdout', _all_output_queue))
    stderr_thread = Thread(target=lambda: _read_stream(process.stderr, _start_time.value, 'stderr', _all_output_queue))

    def _output_queue():
        stdout_thread.start()
        stderr_thread.start()
        _all_output_start.set()
        stdout_thread.join()
        stderr_thread.join()
        resource_measure_thread.join()
        killer_thread.join()
        _all_output_complete.set()

    que_thread = Thread(target=_output_queue)
    que_thread.start()

    # output yield function (can iter output lines)
    def _output_yield():
        _all_output_start.wait()
        while not _all_output_complete.is_set() or not _all_output_queue.empty():
            try:
                _time, _tag, _line = _all_output_queue.get(timeout=0.2)
            except Empty:
                pass
            else:
                yield _time, _tag, _line

        que_thread.join()
        _full_lifetime_complete.set()

    return InteractiveProcess(
        process=process,
        start_time=_start_time.value,
        output_yield_func=_output_yield,
        result_func=lambda: _process_result.value,
        lifetime_event=_full_lifetime_complete,
    )
