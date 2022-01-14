from contextlib import closing
from io import BytesIO, StringIO

import pytest

from pji.control.model import RunResultStatus
from pji.control.run import common_run


@pytest.mark.unittest
class TestControlRunCommon:
    def test_common_run_simple(self):
        with closing(BytesIO(b'1234')) as stdin, closing(BytesIO()) as stdout, closing(BytesIO()) as stderr:
            result = common_run(
                args='cat', shell=True,
                stdin=stdin, stdout=stdout, stderr=stderr,
            )

            assert stdout.getvalue().rstrip(b'\r\n') == b'1234'
            assert stderr.getvalue().rstrip(b'\r\n') == b''
            assert result.ok
            assert result.completed
            assert result.status == RunResultStatus.SUCCESS

    def test_common_run_str(self):
        with closing(StringIO('1234')) as stdin, closing(StringIO()) as stdout, closing(StringIO()) as stderr:
            result = common_run(
                args='cat', shell=True,
                stdin=stdin, stdout=stdout, stderr=stderr,
            )

            assert stdout.getvalue().rstrip('\r\n') == '1234'
            assert stderr.getvalue().rstrip('\r\n') == ''
            assert result.ok
            assert result.completed
            assert result.status == RunResultStatus.SUCCESS

    def test_common_run_without_stdin(self):
        with closing(BytesIO()) as stdout, closing(BytesIO()) as stderr:
            result = common_run(
                args='cat', shell=True,
                stdout=stdout, stderr=stderr,
            )

            assert stdout.getvalue().rstrip(b'\r\n') == b''
            assert stderr.getvalue().rstrip(b'\r\n') == b''
            assert result.ok
            assert result.completed
            assert result.status == RunResultStatus.SUCCESS

    def test_common_run_without_output(self):
        with closing(BytesIO(b'1234')) as stdin:
            result = common_run(
                args='cat', shell=True,
                stdin=stdin,
            )

            assert result.ok
            assert result.completed
            assert result.status == RunResultStatus.SUCCESS

    def test_common_run_with_stderr_content(self):
        with closing(BytesIO(b'1234')) as stdin, closing(BytesIO()) as stdout, closing(BytesIO()) as stderr:
            result = common_run(
                args='python3 -c "import sys;print(123, file=sys.stderr)"',
                stdin=stdin, stdout=stdout, stderr=stderr,
            )

            assert stdout.getvalue().rstrip(b'\r\n') == b''
            assert stderr.getvalue().rstrip(b'\r\n') == b'123'
            assert result.ok
            assert result.completed
            assert result.status == RunResultStatus.SUCCESS

    @pytest.mark.timeout(5.0)
    def test_common_run_rtle(self):
        result = common_run(
            args='python3 -c "while True: pass"',
            resources=dict(max_real_time='2.2s'),
        )

        assert not result.ok
        assert result.completed
        assert result.status == RunResultStatus.REAL_TIME_LIMIT_EXCEED
        assert 2.0 < result.result.real_time < 3.0

    @pytest.mark.flaky(reruns=5)
    @pytest.mark.timeout(5.0)
    def test_common_run_ctle(self):
        result = common_run(
            args='python3 -c "while True: pass"',
            resources=dict(max_cpu_time='2.2s'),
        )

        assert not result.ok
        assert result.completed
        assert result.status == RunResultStatus.CPU_TIME_LIMIT_EXCEED
        assert result.result.cpu_time > 2.2
        assert result.result.signal_code == 9

    @pytest.mark.timeout(5.0)
    def test_common_run_re(self):
        result = common_run(
            args='python3 -c "raise RuntimeError"',
        )

        assert not result.ok
        assert result.completed
        assert result.status == RunResultStatus.RUNTIME_ERROR

    @pytest.mark.timeout(5.0)
    def test_common_run_mle(self):
        result = common_run(
            args='python3 -c "a = [2] * (2 << 24)"',
            resources=dict(max_memory='64mb'),
        )

        assert not result.ok
        assert result.completed
        assert result.status == RunResultStatus.MEMORY_LIMIT_EXCEED
