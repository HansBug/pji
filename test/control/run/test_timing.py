import io
from contextlib import closing

import pytest

from pji.control.model import RunResultStatus
from pji.control.run import timing_run, TimingStdout, TimingStderr, TimingStdin


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestControlRunTiming:
    def test_timing_stdin(self):
        _stdin = b"""
[0.0]echo 233
[0.0]echo 2334
[0.1]whoami
        """

        with closing(io.BytesIO(_stdin)) as stdin:
            si = TimingStdin.load(stdin)
            assert si.str_lines == [
                (0.0, 'echo 233'),
                (0.0, 'echo 2334'),
                (0.1, 'whoami'),
            ]

            order, unorder = False, False
            for i in range(100):
                ssi = si.to_shuffled()
                assert isinstance(ssi, TimingStdin)
                if ssi.str_lines == [
                    (0.0, 'echo 233'),
                    (0.0, 'echo 2334'),
                    (0.1, 'whoami'),
                ]:
                    order = True
                elif ssi.str_lines == [
                    (0.0, 'echo 2334'),
                    (0.0, 'echo 233'),
                    (0.1, 'whoami'),
                ]:
                    unorder = True
                else:
                    pytest.fail('Should not reach here.')

            assert order and unorder

    def test_simple(self):
        _stdin = b"""
[0.0]echo 233
[1.0]echo 2334
[1.5]whoami
        """
        with closing(io.BytesIO(_stdin)) as stdin, \
                closing(io.BytesIO()) as stdout, closing(io.BytesIO()) as stderr:
            result = timing_run(
                args='sh', identification='nobody',
                stdin=stdin, stdout=stdout, stderr=stderr,
            )

            _stdout = TimingStdout.loads(stdout.getvalue())
            assert len(_stdout.lines) == 3
            assert _stdout.lines[0][0] <= _stdout.lines[1][0] <= _stdout.lines[2][0]
            assert 0 <= _stdout.lines[0][0] <= 0.3
            assert _stdout.lines[0][1].rstrip(b'\r\n') == b'233'
            assert 0.9 <= _stdout.lines[1][0] <= 1.3
            assert _stdout.lines[1][1].rstrip(b'\r\n') == b'2334'
            assert 1.5 <= _stdout.lines[2][0] <= 1.8
            assert _stdout.lines[2][1].rstrip(b'\r\n') == b'nobody'

            assert stderr.getvalue().rstrip(b'\r\n') == b''

            assert result.ok
            assert result.completed
            assert result.status == RunResultStatus.SUCCESS

    def test_simple_str(self):
        _stdin = """
[0.0]echo 233
[1.0]echo 2334
[1.5]whoami
        """
        with closing(io.StringIO(_stdin)) as stdin, \
                closing(io.StringIO()) as stdout, closing(io.StringIO()) as stderr:
            result = timing_run(
                args='sh', identification='nobody',
                stdin=stdin, stdout=stdout, stderr=stderr,
            )

            _stdout = TimingStdout.loads(stdout.getvalue())
            assert len(_stdout.lines) == 3
            assert _stdout.lines[0][0] <= _stdout.lines[1][0] <= _stdout.lines[2][0]
            assert 0 <= _stdout.lines[0][0] <= 0.3
            assert _stdout.lines[0][1].rstrip(b'\r\n') == b'233'
            assert 0.9 <= _stdout.lines[1][0] <= 1.3
            assert _stdout.lines[1][1].rstrip(b'\r\n') == b'2334'
            assert 1.5 <= _stdout.lines[2][0] <= 1.8
            assert _stdout.lines[2][1].rstrip(b'\r\n') == b'nobody'

            assert stderr.getvalue().rstrip('\r\n') == ''

            assert result.ok
            assert result.completed
            assert result.status == RunResultStatus.SUCCESS

    def test_simple_with_shuffle(self):
        _stdin = """
[0.0]echo 233
[0.0]echo 2334
[0.1]whoami
            """
        order, unorder = False, False
        for i in range(20):
            if order and unorder:
                break

            with closing(io.StringIO(_stdin)) as stdin, \
                    closing(io.StringIO()) as stdout, closing(io.StringIO()) as stderr:
                result = timing_run(
                    args='sh', identification='nobody',
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    shuffle=True,
                )

                _stdout = TimingStdout.loads(stdout.getvalue())
                assert len(_stdout.lines) == 3
                assert _stdout.lines[0][0] <= _stdout.lines[1][0] <= _stdout.lines[2][0]

                if (0 <= _stdout.lines[0][0] <= 0.3 and _stdout.lines[0][1].rstrip(b'\r\n') == b'233') and \
                        (0 <= _stdout.lines[1][0] <= 0.3 and _stdout.lines[1][1].rstrip(b'\r\n') == b'2334'):
                    order = True
                elif (0 <= _stdout.lines[0][0] <= 0.3 and _stdout.lines[0][1].rstrip(b'\r\n') == b'2334') and \
                        (0 <= _stdout.lines[1][0] <= 0.3 and _stdout.lines[1][1].rstrip(b'\r\n') == b'233'):
                    unorder = True
                else:
                    pytest.fail('Should not reach here.')

                assert 0.1 <= _stdout.lines[2][0] <= 0.5
                assert _stdout.lines[2][1].rstrip(b'\r\n') == b'nobody'

                assert stderr.getvalue().rstrip('\r\n') == ''

                assert result.ok
                assert result.completed
                assert result.status == RunResultStatus.SUCCESS

        assert order and unorder

    def test_with_stderr(self):
        with closing(io.BytesIO()) as stdout, closing(io.BytesIO()) as stderr:
            result = timing_run(
                args='python3 -c "import time, sys;print(233, flush=True);time.sleep(1.0);'
                     'print(2334, file=sys.stderr, flush=True);"', identification='nobody',
                stdout=stdout, stderr=stderr,
            )

            _stdout = TimingStdout.loads(stdout.getvalue())
            assert len(_stdout.lines) == 1
            assert 0 <= _stdout.lines[0][0] <= 0.3
            assert _stdout.lines[0][1].rstrip(b'\r\n') == b'233'

            _stderr = TimingStderr.loads(stderr.getvalue())
            assert len(_stderr.lines) == 1
            assert 1.0 <= _stderr.lines[0][0] <= 1.3
            assert _stderr.lines[0][1].rstrip(b'\r\n') == b'2334'

            assert result.ok
            assert result.completed
            assert result.status == RunResultStatus.SUCCESS

    def test_with_break(self):
        _stdin = b"""
        [0.0]echo 233
        [1.0]echo 2334
        [1.5]whoami
                """
        with closing(io.BytesIO(_stdin)) as stdin, \
                closing(io.BytesIO()) as stdout, closing(io.BytesIO()) as stderr:
            result = timing_run(
                args='sh', identification='nobody', resources=dict(max_real_time='0.75s'),
                stdin=stdin, stdout=stdout, stderr=stderr,
            )

            _stdout = TimingStdout.loads(stdout.getvalue())
            assert len(_stdout.lines) == 1
            assert 0 <= _stdout.lines[0][0] <= 0.3
            assert _stdout.lines[0][1].rstrip(b'\r\n') == b'233'

            assert stderr.getvalue().rstrip(b'\r\n') == b''

            assert not result.ok
            assert result.completed
            assert result.status == RunResultStatus.REAL_TIME_LIMIT_EXCEED
