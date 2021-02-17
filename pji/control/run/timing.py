import io
import time

from .encoding import _try_write, _try_read_to_bytes
from ..model import RunResult
from ..model import TimingContent as _AbstractTimingContent
from ..process import interactive_process
from ...utils import eclosing


class TimingStdin(_AbstractTimingContent):
    pass


class TimingStdout(_AbstractTimingContent):
    pass


class TimingStderr(_AbstractTimingContent):
    pass


def timing_run(args, shell: bool = False, stdin=None, stdout=None, stderr=None,
               environ=None, cwd=None, resources=None, identification=None) -> RunResult:
    """
    Create an common process with stream
    :param args: arguments for execution
    :param shell: use shell to execute args
    :param stdin: stdin stream (none means nothing)
    :param stdout: stdout stream (none means nothing)
    :param stderr: stderr stream (none means nothing)
    :param environ: environment variables
    :param cwd: new work dir
    :param resources: resource limit
    :param identification: user and group for execution
    :return: run result of this time
    """
    stdin_need_close = not stdin
    stdin = stdin or io.BytesIO()

    stdout_need_close = not stdout
    stdout = stdout or io.BytesIO()

    stderr_need_close = not stderr
    stderr = stderr or io.BytesIO()

    with eclosing(stdin, stdin_need_close) as stdin, \
            eclosing(stdout, stdout_need_close) as stdout, \
            eclosing(stderr, stderr_need_close) as stderr:
        with interactive_process(
                args=args, shell=shell,
                environ=environ, cwd=cwd,
                resources=resources, identification=identification,
        ) as ip:
            _stdin = TimingStdin.loads(_try_read_to_bytes(stdin))
            for _time, _line in _stdin.lines:
                _target_time = ip.start_time + _time
                while time.time() < _target_time and not ip.completed:
                    time.sleep(max(min(0.2, _target_time - time.time()), 0.0))

                if not ip.completed:
                    try:
                        ip.print_stdin(_line)
                    except BrokenPipeError:
                        break
                else:
                    break

            ip.close_stdin()

            _stdout, _stderr = [], []
            for _time, _tag, _line in ip.output_yield:
                if _tag == 'stdout':
                    _stdout.append((_time, _line))
                elif _tag == 'stderr':
                    _stderr.append((_time, _line))
                else:
                    raise ValueError('Unknown output type - {type}.'.format(type=repr(_time)))

            ip.join()
            _try_write(stdout, TimingStdout.loads(_stdout).dumps())
            _try_write(stderr, TimingStderr.loads(_stderr).dumps())

            return ip.result
