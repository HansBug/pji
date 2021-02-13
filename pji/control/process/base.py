import os
import signal
import time
from multiprocessing import Event, Value
from multiprocessing.synchronize import Event as EventClass
from threading import Thread
from typing import Callable, Tuple, Optional

from ..model import ProcessResult
from ...utils import ValueProxy


def read_all_from_stream(stream) -> bytes:
    return b''.join([line for line in stream])


def measure_thread(start_time_ok: Event, start_time: Value, child_pid: int) \
        -> Tuple[Thread, EventClass, EventClass, EventClass, ValueProxy]:
    _process_result = ValueProxy()
    _process_complete = Event()
    _measure_initialized = Event()
    _measure_complete = Event()

    def _thread_func():
        _measure_initialized.set()
        _, status, resource_usage = os.wait4(child_pid, os.WSTOPPED)
        _process_complete.set()
        start_time_ok.wait()
        _process_result.value = ProcessResult(status, start_time.value, time.time(), resource_usage)
        _measure_complete.set()

    return Thread(target=_thread_func), _measure_initialized, _process_complete, _measure_complete, _process_result


def killer_thread(start_time_ok: Event, start_time: Value, child_pid: int,
                  real_time_limit: float, process_complete: Event) -> Tuple[Thread, EventClass]:
    _killer_initialized = Event()

    def _thread_func():
        _killer_initialized.set()
        if real_time_limit is not None:
            start_time_ok.wait()
            target_time = start_time.value + real_time_limit
            while time.time() < target_time and not process_complete.is_set():
                time.sleep(min(max(target_time - time.time(), 0.0), 0.2))
            if not process_complete.is_set():
                os.kill(child_pid, signal.SIGKILL)
                process_complete.wait()

    return Thread(target=_thread_func), _killer_initialized


def preexec_fn_merge(preexec_fn: Optional[Callable[[], None]]) -> Tuple[Event, Value, Callable[[], None]]:
    _start_time_ok = Event()
    _start_time = Value('d', 0.0)

    def _preexec_fn():
        if preexec_fn is not None:
            preexec_fn()
        _start_time.value = time.time()
        _start_time_ok.set()

    return _start_time_ok, _start_time, _preexec_fn
