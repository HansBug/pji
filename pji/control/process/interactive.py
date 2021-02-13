import subprocess
import time
from multiprocessing import Event
from multiprocessing.synchronize import Event as EventClass
from queue import Queue, Empty
from threading import Thread
from typing import Optional, Mapping

from .base import BYTES_LINESEQ
from ..model import ProcessResult


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

    def print_stdin(self, line: bytes, flush: bool = True, end: bytes = BYTES_LINESEQ):
        self.__process.stdin.write(line + end)
        if flush:
            self.__process.stdin.flush()

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


def interactive_process(args, preexec_fn=None, real_time_limit=None,
                        environ: Optional[Mapping[str, str]] = None) -> InteractiveProcess:
    _full_lifetime_complete = Event()
    environ = dict(environ or {})
    pass

    # if not arg_file:
    #     raise EnvironmentError('Executable {exec} not found.'.format(exec=args[0]))
    #
    # _parent_initialized = Event()
    # _start_time = Value('d', 0.0)
    # _start_time_ok = Event()
    #
    # return InteractiveProcess(
    #     process=process,
    #     start_time=_start_time.value,
    #     output_yield_func=_output_yield,
    #     result_func=lambda: _process_result.value,
    #     lifetime_event=_full_lifetime_complete,
    # )
