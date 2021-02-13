import os
from multiprocessing import Event, Value
from multiprocessing.synchronize import Event as EventClass
from queue import Queue, Empty
from threading import Thread
from typing import Optional, Mapping

from .base import BYTES_LINESEQ, measure_thread, killer_thread, load_lines_from_bytes_stream
from .executor import get_executor_func
from ..model import ProcessResult


class InteractiveProcess:
    def __init__(self, stdin_stream, start_time: float,
                 output_iter, result_func, lifetime_event: EventClass):
        self.__stdin_stream = stdin_stream
        self.__start_time = start_time
        self.__output_iter = output_iter
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
        return self.__output_iter

    def print_stdin(self, line: bytes, flush: bool = True, end: bytes = BYTES_LINESEQ):
        self.__stdin_stream.write(line + end)
        if flush:
            self.__stdin_stream.flush()

    def close_stdin(self):
        self.__stdin_stream.close()

    def join(self):
        return self.__lifetime_event.wait()


def _read_stream(pipe_entry, start_time_ok: EventClass, start_time: Value, tag: str, queue: Queue):
    def _transform_func(item):
        _time, _line = item
        return _time - start_time.value, tag, _line.rstrip(b'\r\n')

    with os.fdopen(pipe_entry, 'rb', 0) as stream:
        start_time_ok.wait()
        return load_lines_from_bytes_stream(stream, queue, _transform_func)


# noinspection DuplicatedCode
def interactive_process(args, preexec_fn=None, real_time_limit=None,
                        environ: Optional[Mapping[str, str]] = None) -> InteractiveProcess:
    _full_lifetime_complete = Event()
    environ = dict(environ or {})

    _parent_initialized = Event()
    _start_time = Value('d', 0.0)
    _start_time_ok = Event()

    # noinspection DuplicatedCode
    def _execute_parent() -> InteractiveProcess:
        os.close(stdin_read)
        os.close(stdout_write)
        os.close(stderr_write)

        # measure thread
        _measure_thread, _measure_initialized, _process_complete, _measure_complete, _result_proxy = measure_thread(
            start_time_ok=_start_time_ok,
            start_time=_start_time,
            child_pid=child_pid,
        )
        _measure_thread.start()

        # killer thread
        _killer_thread, _killer_initialized = killer_thread(
            start_time_ok=_start_time_ok,
            start_time=_start_time,
            child_pid=child_pid,
            real_time_limit=real_time_limit,
            process_complete=_process_complete,
        )
        _killer_thread.start()

        # lines output
        _output_queue = Queue()
        _output_start, _output_complete = Event(), Event()
        _start_time_ok.wait()
        _stdout_thread = Thread(
            target=lambda: _read_stream(stdout_read, _start_time_ok, _start_time, 'stdout', _output_queue))
        _stderr_thread = Thread(
            target=lambda: _read_stream(stderr_read, _start_time_ok, _start_time, 'stderr', _output_queue))

        def _output_queue_func():
            _stdout_thread.start()
            _stderr_thread.start()
            _output_start.set()

            _stdout_thread.join()
            _stderr_thread.join()
            _output_complete.set()

        _queue_thread = Thread(target=_output_queue_func)
        _queue_thread.start()

        def _output_yield():
            _output_start.wait()
            while not _output_complete.is_set() or not _output_queue.empty():
                try:
                    _time, _tag, _line = _output_queue.get(timeout=0.2)
                except Empty:
                    pass
                else:
                    yield _time, _tag, _line

            _measure_thread.join()
            _killer_thread.join()
            _queue_thread.join()
            _full_lifetime_complete.set()

        _stdin_stream = os.fdopen(stdin_write, 'wb', 0)
        _output_iter = _output_yield()

        # wait for all the thread initialized
        _measure_initialized.wait()
        _killer_initialized.wait()
        _output_start.wait()
        _parent_initialized.set()

        _start_time_ok.wait()
        return InteractiveProcess(
            stdin_stream=_stdin_stream,
            start_time=_start_time.value,
            output_iter=_output_iter,
            result_func=lambda: _result_proxy.value,
            lifetime_event=_full_lifetime_complete,
        )

    stdin_read, stdin_write = os.pipe()
    stdout_read, stdout_write = os.pipe()
    stderr_read, stderr_write = os.pipe()

    _execute_child = get_executor_func(
        args, dict(environ or {}), preexec_fn,
        _parent_initialized,
        _start_time_ok, _start_time,
        (stdin_read, stdin_write),
        (stdout_read, stdout_write),
        (stderr_read, stderr_write),
    )

    child_pid = os.fork()

    if not child_pid:
        _execute_child()
    else:
        return _execute_parent()
