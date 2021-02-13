import os
import time

import pytest

from pji.control.process import common_process, CommonProcess


@pytest.mark.unittest
class TestControlProcessCommon:
    def test_common_process_simple(self):
        _start = time.time()
        cp = common_process(
            args='echo 233',
        )
        assert isinstance(cp, CommonProcess)
        assert abs(_start - cp.start_time) < 0.2

        _cresult = cp.communicate()
        assert cp.stdin == b''
        assert cp.stdout.decode().strip() == '233'
        assert cp.stderr.decode().strip() == ''

        assert _cresult is not None
        _stdout, _stderr = _cresult
        assert _stdout == cp.stdout
        assert _stderr == cp.stderr

        _result = cp.result
        assert _result is not None
        assert _result.ok
        assert _result.cpu_time < 0.5

    def test_common_process_with_input(self):
        _start = time.time()
        cp = common_process(
            args="python3 -c \"print(sum([int(value) for value in input().split(' ')]))\""
        )
        assert isinstance(cp, CommonProcess)
        assert abs(_start - cp.start_time) < 0.2

        _cresult = cp.communicate(b'2 3 4 5 6')
        assert cp.stdin == b'2 3 4 5 6'
        assert cp.stdout.decode().strip() == '20'
        assert cp.stderr.decode().strip() == ''

        assert _cresult is not None
        _stdout, _stderr = _cresult
        assert _stdout == cp.stdout
        assert _stderr == cp.stderr

        cp.join()
        _result = cp.result
        assert _result is not None
        assert _result.ok
        assert _result.cpu_time < 0.5

    def test_common_process_without_wait(self):
        _start = time.time()
        cp = common_process(
            args="python3 -c \"print(sum([int(value) for value in input().split(' ')]))\""
        )
        assert isinstance(cp, CommonProcess)
        assert abs(_start - cp.start_time) < 0.2

        _cresult = cp.communicate(b'2 3 4 5 6', wait=False)
        cp.join()
        assert cp.stdin == b'2 3 4 5 6'
        assert cp.stdout.decode().strip() == '20'
        assert cp.stderr.decode().strip() == ''

        assert _cresult is None

        cp.join()
        _result = cp.result
        assert _result is not None
        assert _result.ok
        assert _result.cpu_time < 0.5

    def test_common_process_rtle(self):
        _start = time.time()
        cp = common_process(
            args="python3 -c \"print(sum([int(value) for value in input().split(' ')]))\";import time;time.sleep(4.0);",
            real_time_limit=2.0
        )
        assert isinstance(cp, CommonProcess)
        assert abs(_start - cp.start_time) < 0.2

        cp.communicate(b'2 3 4 5 6')
        cp.join()

        _result = cp.result
        assert not _result.ok
        assert _result.signal_code == 0
        assert _result.exitcode == 1


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
