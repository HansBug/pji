import os
import sys
import time
from multiprocessing import Event, Value
from multiprocessing.synchronize import Event as EventClass
from threading import Thread
from typing import Optional, Tuple, Mapping

import where

from .base import measure_thread, killer_thread, read_all_from_stream
from ..model import ProcessResult
from ...utils import ValueProxy, args_split


class CommonProcess:
    def __init__(self, start_time: float,
                 communicate_event: EventClass, communicate_complete: EventClass,
                 communicate_stdin: ValueProxy, communicate_stdout: ValueProxy, communicate_stderr: ValueProxy,
                 result_func, lifetime_event: EventClass):
        self.__start_time = start_time

        self.__communicate_event = communicate_event
        self.__communicate_complete = communicate_complete
        self.__communicate_stdin = communicate_stdin
        self.__communicate_stdout = communicate_stdout
        self.__communicate_stderr = communicate_stderr

        self.__result_func = result_func
        self.__lifetime_event = lifetime_event

    def communicate(self, stdin: Optional[bytes] = None, wait: bool = True) -> Optional[Tuple[bytes, bytes]]:
        self.__communicate_stdin.value = stdin or b''
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


def common_process(args, preexec_fn=None, real_time_limit=None,
                   environ: Optional[Mapping[str, str]] = None) -> CommonProcess:
    _full_lifetime_complete = Event()
    args = args_split(args)
    arg_file = where.first(args[0])
    environ = dict(environ or {})

    if not arg_file:
        raise EnvironmentError('Executable {exec} not found.'.format(exec=args[0]))

    _parent_initialized = Event()
    _start_time = Value('d', 0.0)
    _start_time_ok = Event()

    def _execute_child():
        os.close(stdin_write)
        os.dup2(stdin_read, sys.stdin.fileno())

        os.close(stdout_read)
        os.dup2(stdout_write, sys.stdout.fileno())

        os.close(stderr_read)
        os.dup2(stderr_write, sys.stderr.fileno())

        if preexec_fn is not None:
            preexec_fn()

        _parent_initialized.wait()
        _start_time.value = time.time()
        _start_time_ok.set()

        os.execvpe(arg_file, args, environ)

    def _execute_parent() -> CommonProcess:
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

        # communication thread
        _communicate_initialized, _communicate_event, _communicate_complete = Event(), Event(), Event()
        _communicate_stdin, _communicate_stdout, _communicate_stderr = ValueProxy(), ValueProxy(), ValueProxy()

        def _communicate_func():
            with os.fdopen(stdin_write, 'wb', 0) as fstdin, \
                    os.fdopen(stdout_read, 'rb', 0) as fstdout, \
                    os.fdopen(stderr_read, 'rb', 0) as fstderr:
                _communicate_initialized.set()
                _communicate_event.wait()

                _stdout, _stderr = None, None

                def _read_stdout():
                    nonlocal _stdout
                    _stdout = read_all_from_stream(fstdout)

                def _read_stderr():
                    nonlocal _stderr
                    _stderr = read_all_from_stream(fstderr)

                _stdout_thread = Thread(target=_read_stdout)
                _stderr_thread = Thread(target=_read_stderr)

                # write stdin into stream
                fstdin.write(_communicate_stdin.value)
                fstdin.flush()
                _stdout_thread.start()
                _stderr_thread.start()

                # waiting for receiving of stdout and stderr
                fstdin.close()
                _stdout_thread.join()
                _stderr_thread.join()

                # set stderr
                _communicate_stdout.value = _stdout
                _communicate_stderr.value = _stderr
                _communicate_complete.set()

                # ending of all the process
                _process_complete.wait()
                _measure_complete.wait()
                _full_lifetime_complete.set()

        _communicate_thread = Thread(target=_communicate_func)
        _communicate_thread.start()

        _measure_initialized.wait()
        _killer_initialized.wait()
        _communicate_initialized.wait()
        _parent_initialized.set()

        _start_time_ok.wait()
        return CommonProcess(
            start_time=_start_time.value,
            communicate_event=_communicate_event,
            communicate_complete=_communicate_complete,
            communicate_stdin=_communicate_stdin,
            communicate_stdout=_communicate_stdout,
            communicate_stderr=_communicate_stderr,
            result_func=lambda: _result_proxy.value,
            lifetime_event=_full_lifetime_complete,
        )

    stdin_read, stdin_write = os.pipe()
    stdout_read, stdout_write = os.pipe()
    stderr_read, stderr_write = os.pipe()
    child_pid = os.fork()

    if not child_pid:
        _execute_child()
    else:
        return _execute_parent()
