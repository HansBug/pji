import subprocess
from multiprocessing import Event
from multiprocessing.synchronize import Event as EventClass
from subprocess import Popen
from threading import Thread
from typing import Optional, Tuple

from .base import process_kill_thread, wait_and_measure_thread, preexec_fn_merge
from ..model import ProcessResult
from ...utils import args_split, ValueProxy


class CommonProcess:
    def __init__(self, process: Popen, start_time: float,
                 communicate_event: EventClass, communicate_complete: EventClass,
                 communicate_stdin: ValueProxy, communicate_stdout: ValueProxy, communicate_stderr: ValueProxy,
                 result_func, lifetime_event: EventClass):
        self.__process = process
        self.__start_time = start_time

        self.__communicate_event = communicate_event
        self.__communicate_complete = communicate_complete
        self.__communicate_stdin = communicate_stdin
        self.__communicate_stdout = communicate_stdout
        self.__communicate_stderr = communicate_stderr

        self.__result_func = result_func
        self.__lifetime_event = lifetime_event

    def communicate(self, stdin: bytes, wait: bool = True) -> Optional[Tuple[bytes, bytes]]:
        self.__communicate_stdin.value = stdin
        self.__communicate_event.set()

        if wait:
            self.__communicate_complete.wait()
            return self.__communicate_stdout.value, self.__communicate_stderr.value
        else:
            return None

    @property
    def start_time(self) -> float:
        return self.__start_time

    @property
    def result(self) -> ProcessResult:
        return self.__result_func()

    @property
    def stdin(self) -> Optional[bytes]:
        return self.__communicate_stdin.value

    @property
    def stdout(self) -> Optional[bytes]:
        return self.__communicate_stdout.value

    @property
    def stderr(self) -> Optional[bytes]:
        return self.__communicate_stderr.value

    def join(self):
        self.__lifetime_event.wait()


def common_process(args, preexec_fn=None, real_time_limit=None) -> CommonProcess:
    _full_lifetime_complete = Event()
    _start_time_ok, _start_time, _before_exec = preexec_fn_merge(preexec_fn)

    process = subprocess.Popen(
        args=args_split(args),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=_before_exec,
    )

    # thread for process control and resource measure
    resource_measure_thread, _process_complete, _process_result = \
        wait_and_measure_thread(_start_time_ok, _start_time, process)
    resource_measure_thread.start()

    # thread for killing the process when real time exceed
    killer_thread = process_kill_thread(_start_time_ok, _start_time, process, real_time_limit, _process_complete)
    killer_thread.start()

    # communication function control
    _communicate_stdin, _communicate_stdout, _communicate_stderr = ValueProxy(), ValueProxy(), ValueProxy()
    _communicate_event, _communicate_complete = Event(), Event()

    def _communicate_func():
        _start_time_ok.wait()
        _communicate_event.wait()
        _stdout, _stderr = process.communicate(_communicate_stdin.value)
        _communicate_stdout.value = _stdout
        _communicate_stderr.value = _stderr
        _communicate_complete.set()

        resource_measure_thread.join()
        killer_thread.join()
        _full_lifetime_complete.set()

    communicate_thread = Thread(target=_communicate_func)

    # wait for real start
    _start_time_ok.wait()
    communicate_thread.start()

    return CommonProcess(
        process=process,
        start_time=_start_time.value,
        communicate_event=_communicate_event,
        communicate_complete=_communicate_complete,
        communicate_stdin=_communicate_stdin,
        communicate_stdout=_communicate_stdout,
        communicate_stderr=_communicate_stderr,
        result_func=lambda: _process_result.value,
        lifetime_event=_full_lifetime_complete,
    )
