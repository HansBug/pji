import os
import signal
import time
from multiprocessing import Event, Value
from subprocess import Popen
from threading import Thread
from typing import Callable, Tuple, Optional

from ..model import ProcessResult
from ...utils import ValueProxy


def wait_and_measure_thread(start_time_ok: Event, start_time: Value, process: Popen) \
        -> Tuple[Thread, Event, ValueProxy]:
    _process_result = ValueProxy()
    _process_complete = Event()

    def _thread_func():
        start_time_ok.wait()
        _, status, resource_usage = os.wait4(process.pid, os.WSTOPPED)
        _process_complete.set()
        _process_result.value = ProcessResult(status, start_time.value, time.time(), resource_usage)

    return Thread(target=_thread_func), _process_complete, _process_result


def process_kill_thread(start_time_ok: Event, start_time: Value, process: Popen,
                        real_time_limit: float, process_complete: Event) -> Thread:
    def _thread_func():
        start_time_ok.wait()
        if real_time_limit is not None:
            time.sleep(max(start_time.value + real_time_limit - time.time(), 0.0))
            if not process_complete.is_set():
                os.kill(process.pid, signal.SIGKILL)
                process_complete.wait()

    return Thread(target=_thread_func)


def preexec_fn_merge(preexec_fn: Optional[Callable[[], None]]) -> Tuple[Event, Value, Callable[[], None]]:
    _start_time_ok = Event()
    _start_time = Value('d', 0.0)

    def _preexec_fn():
        if preexec_fn is not None:
            preexec_fn()
        _start_time.value = time.time()
        _start_time_ok.set()

    return _start_time_ok, _start_time, _preexec_fn
