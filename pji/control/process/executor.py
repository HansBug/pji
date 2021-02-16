import os
import sys
import time
from multiprocessing import Value, Queue
from multiprocessing.synchronize import Event as EventClass
from typing import Mapping

import where

from ...utils import args_split


class ExecutorException(Exception):
    def __init__(self, exception):
        self.__exception = exception
        Exception.__init__(self, repr(exception))

    @property
    def exception(self):
        return self.__exception


def get_child_executor_func(args, shell: bool, environ: Mapping[str, str], preexec_fn,
                            executor_prepare_ok: EventClass, executor_has_exception: EventClass,
                            executor_exceptions: Queue,
                            parent_initialized: EventClass,
                            start_time_ok: EventClass, start_time: Value,
                            stdin_pipes, stdout_pipes, stderr_pipes):
    if shell:
        if isinstance(args, str):
            if where.first('sh'):
                args = [where.first('sh'), '-c', args]
            elif where.first('cmd'):
                args = [where.first('cmd'), '/c', args]
            else:
                raise EnvironmentError('Neither shell nor cmd found in this environment.')
        else:
            raise ValueError(
                'When shell is enabled, args should be str but {actual} found.'.format(actual=repr(type(args))))
    else:
        args = args_split(args)
    arg_file = where.first(args[0])

    if not arg_file:
        raise EnvironmentError('Executable {exec} not found.'.format(exec=args[0]))

    stdin_read, stdin_write = stdin_pipes
    stdout_read, stdout_write = stdout_pipes
    stderr_read, stderr_write = stderr_pipes

    def _execute_child():
        os.close(stdin_write)
        os.dup2(stdin_read, sys.stdin.fileno())

        os.close(stdout_read)
        os.dup2(stdout_write, sys.stdout.fileno())

        os.close(stderr_read)
        os.dup2(stderr_write, sys.stderr.fileno())

        _exception = None
        try:
            if preexec_fn is not None:
                preexec_fn()
        except Exception as err:
            _exception = err

        if _exception is not None:
            executor_has_exception.set()
            executor_exceptions.put(ExecutorException(_exception))
        executor_prepare_ok.set()

        if _exception is None:
            parent_initialized.wait()
            start_time.value = time.time()
            start_time_ok.set()

            os.execvpe(arg_file, args, environ)

    return _execute_child
