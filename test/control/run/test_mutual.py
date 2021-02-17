import io
import os
import sys
from contextlib import closing

import pytest

from pji.control.model import RunResultStatus
from pji.control.run import mutual_run, MutualStdout, MutualStderr

demo_value = 1


def demo_mutual_func():
    print("echo 233")
    print("line:", input(), file=sys.stderr)
    print("echo stderr 1>&2")
    print("whoami")
    print("line:", input(), file=sys.stderr)


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestControlRunMutual:
    def test_simple(self):
        with closing(io.BytesIO()) as stdout, closing(io.BytesIO()) as stderr:
            result = mutual_run(
                args='sh',
                identification='nobody',
                stdin=demo_mutual_func, stdout=stdout, stderr=stderr,
            )

            _stdout = MutualStdout.loads(stdout.getvalue())
            assert len(_stdout.lines) == 2
            assert _stdout.lines[0][1].rstrip(b'\r\n') == b'line: 233'
            assert _stdout.lines[1][1].rstrip(b'\r\n') == b'line: nobody'

            _stderr = MutualStderr.loads(stderr.getvalue())
            assert len(_stderr.lines) == 1
            assert _stderr.lines[0][1].rstrip(b'\r\n') == b'stderr'

            assert result.ok
            assert result.completed
            assert result.status == RunResultStatus.ACCEPTED

    def test_simple_str_stdin(self):
        with closing(io.BytesIO()) as stdout, closing(io.BytesIO()) as stderr:
            result = mutual_run(
                args='sh',
                identification='nobody',
                stdin='test.control.run.test_mutual:demo_mutual_func', stdout=stdout, stderr=stderr,
            )

            _stdout = MutualStdout.loads(stdout.getvalue())
            assert len(_stdout.lines) == 2
            assert _stdout.lines[0][1].rstrip(b'\r\n') == b'line: 233'
            assert _stdout.lines[1][1].rstrip(b'\r\n') == b'line: nobody'

            _stderr = MutualStderr.loads(stderr.getvalue())
            assert len(_stderr.lines) == 1
            assert _stderr.lines[0][1].rstrip(b'\r\n') == b'stderr'

            assert result.ok
            assert result.completed
            assert result.status == RunResultStatus.ACCEPTED

    def test_invalid_str_not_exist(self):
        with pytest.raises(AttributeError):
            with closing(io.BytesIO()) as stdout, closing(io.BytesIO()) as stderr:
                mutual_run(
                    args='sh',
                    identification='nobody',
                    stdin='test.control.run.test_mutual:demo_mutual_funcxxxx', stdout=stdout, stderr=stderr,
                )

    def test_invalid_str_not_callable(self):
        with pytest.raises(TypeError):
            with closing(io.BytesIO()) as stdout, closing(io.BytesIO()) as stderr:
                mutual_run(
                    args='sh',
                    identification='nobody',
                    stdin='test.control.run.test_mutual:demo_value', stdout=stdout, stderr=stderr,
                )

    def test_invalid_str_invalid(self):
        with pytest.raises(ValueError):
            with closing(io.BytesIO()) as stdout, closing(io.BytesIO()) as stderr:
                mutual_run(
                    args='sh',
                    identification='nobody',
                    stdin='test.control.run.test_mutual.demo_mutual_funcxxxx', stdout=stdout, stderr=stderr,
                )

    def test_invalid_type(self):
        with pytest.raises(TypeError):
            with closing(io.BytesIO()) as stdout, closing(io.BytesIO()) as stderr:
                mutual_run(
                    args='sh',
                    identification='nobody',
                    stdin=1, stdout=stdout, stderr=stderr,
                )

    def test_nothing(self):
        with closing(io.BytesIO()) as stdout, closing(io.BytesIO()) as stderr:
            result = mutual_run(
                args='echo 233 1>&2', shell=True,
                identification='nobody',
                stdout=stdout, stderr=stderr,
            )

            _stdout = MutualStdout.loads(stdout.getvalue())
            assert len(_stdout.lines) == 0

            _stderr = MutualStderr.loads(stderr.getvalue())
            assert len(_stderr.lines) == 1
            assert _stderr.lines[0][1].rstrip(b'\r\n') == b'233'

            assert result.ok
            assert result.completed
            assert result.status == RunResultStatus.ACCEPTED

    def test_process_killed(self):
        def _func():
            import time
            _start_time = time.time()
            while time.time() < _start_time + 1.0:
                print("echo 233 1>&2", flush=True)
                time.sleep(0.05)

        with closing(io.BytesIO()) as stdout, closing(io.BytesIO()) as stderr:
            result = mutual_run(
                args='sh',
                identification='nobody',
                resources=dict(max_real_time='0.5s'),
                stdin=_func, stdout=stdout, stderr=stderr,
            )

            _stdout = MutualStdout.loads(stdout.getvalue())
            assert len(_stdout.lines) == 0

            _stderr = MutualStderr.loads(stderr.getvalue())
            assert 7 <= len(_stderr.lines) <= 13

            assert not result.ok
            assert result.completed
            assert result.status == RunResultStatus.REAL_TIME_LIMIT_EXCEED

    def test_script_quit(self):
        with closing(io.BytesIO()) as stdout, closing(io.BytesIO()) as stderr:
            result = mutual_run(
                args='seq 1 2000 | xargs -n 1', shell=True,
                identification='nobody',
                stdout=stdout, stderr=stderr,
            )

            _stdout = MutualStdout.loads(stdout.getvalue())
            assert len(_stdout.lines) == 0

            _stderr = MutualStderr.loads(stderr.getvalue())
            assert len(_stdout.lines) == 0

            assert result.ok
            assert result.completed
            assert result.status == RunResultStatus.ACCEPTED


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
