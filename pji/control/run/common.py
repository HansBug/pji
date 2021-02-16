import io
from typing import Mapping, Optional

from ..model import ResourceLimit, Identification
from ..process import common_process


def common_run(args, shell: bool = False,
               stdin=None, stdout=None, stderr=None,
               environ: Optional[Mapping[str, str]] = None, cwd: Optional[str] = None,
               resources: Optional[ResourceLimit] = None, identification: Optional[Identification] = None
               ):
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
    :return: CommonProcess object to do run
    """

    stdin = stdin or io.BytesIO()
    stdout = stdout or io.BytesIO()
    stderr = stderr or io.BytesIO()

    with common_process(
            args=args, shell=shell,
            environ=environ, cwd=cwd,
            resources=resources, identification=identification,
    ) as cp:
        cp.communicate(stdin.read(), wait=False)
        cp.join()

        stdout.write(cp.stdout)
        stderr.write(cp.stderr)
