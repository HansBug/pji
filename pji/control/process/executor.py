import os
import sys
import time
from multiprocessing import Value
from multiprocessing.synchronize import Event as EventClass
from typing import Mapping

import where

from ...utils import args_split


def get_executor_func(args, environ: Mapping[str, str], preexec_fn,
                      parent_initialized: EventClass,
                      start_time_ok: EventClass, start_time: Value,
                      stdin_pipes, stdout_pipes, stderr_pipes):
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

        if preexec_fn is not None:
            preexec_fn()

        parent_initialized.wait()
        start_time.value = time.time()
        start_time_ok.set()

        os.execvpe(arg_file, args, environ)

    return _execute_child
