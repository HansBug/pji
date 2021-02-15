import os
import time

import pytest

from pji.control import ResourceLimit, common_process, CommonProcess


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestControlProcessCommon:
    def test_common_process_simple(self):
        _before_start = time.time()
        with common_process(
                args='echo 233',
        ) as cp:
            _after_start = time.time()
            assert isinstance(cp, CommonProcess)
            assert _before_start <= cp.start_time <= _after_start

            _cresult = cp.communicate()
            assert cp.stdin == b''
            assert cp.stdout.decode().strip() == '233'
            assert cp.stderr.decode().strip() == ''

            assert _cresult is not None
            _stdout, _stderr = _cresult
            assert _stdout == cp.stdout
            assert _stderr == cp.stderr

            cp.join()
            _result = cp.process_result
            assert _result is not None
            assert _result.ok
            assert _result.cpu_time < 0.5

    def test_common_process_with_env(self):
        _before_start = time.time()
        with common_process(
                args="sh -c 'echo ${ENV_TEST}'",
                environ={'ENV_TEST': '233'},
        ) as cp:
            _after_start = time.time()
            assert isinstance(cp, CommonProcess)
            assert _before_start <= cp.start_time <= _after_start

            _cresult = cp.communicate()
            assert cp.stdin == b''
            assert cp.stdout.decode().strip() == '233'
            assert cp.stderr.decode().strip() == ''

            assert _cresult is not None
            _stdout, _stderr = _cresult
            assert _stdout == cp.stdout
            assert _stderr == cp.stderr

            cp.join()
            _result = cp.process_result
            assert _result is not None
            assert _result.ok
            assert _result.cpu_time < 0.5

    def test_common_process_with_input(self):
        _before_start = time.time()
        with common_process(
                args="python3 -c \"print(sum([int(value) for value in input().split(' ')]))\""
        ) as cp:
            _after_start = time.time()
            assert isinstance(cp, CommonProcess)
            assert _before_start <= cp.start_time <= _after_start

            _cresult = cp.communicate(b'2 3 4 5 6')
            assert cp.stdin == b'2 3 4 5 6'
            assert cp.stdout.decode().strip() == '20'
            assert cp.stderr.decode().strip() == ''

            assert _cresult is not None
            _stdout, _stderr = _cresult
            assert _stdout == cp.stdout
            assert _stderr == cp.stderr

            cp.join()
            _result = cp.process_result
            assert _result is not None
            assert _result.ok
            assert _result.cpu_time < 0.5

    def test_common_process_without_wait(self):
        _before_start = time.time()
        with common_process(
                args="python3 -c \"print(sum([int(value) for value in input().split(' ')]))\""
        ) as cp:
            _after_start = time.time()
            assert isinstance(cp, CommonProcess)
            assert _before_start <= cp.start_time <= _after_start

            _cresult = cp.communicate(b'2 3 4 5 6', wait=False)
            cp.join()
            assert cp.stdin == b'2 3 4 5 6'
            assert cp.stdout.decode().strip() == '20'
            assert cp.stderr.decode().strip() == ''

            assert _cresult is None

            cp.join()
            _result = cp.process_result
            assert _result is not None
            assert _result.ok
            assert _result.cpu_time < 0.5

    def test_common_process_rtle(self):
        _before_start = time.time()
        with common_process(
                args="python3 -c \"print(sum([int(value) for value in input().split(' ')]));"
                     "import time;time.sleep(4.0);\"",
                resources=ResourceLimit(
                    max_real_time='2s',
                )
        ) as cp:
            _after_start = time.time()
            assert isinstance(cp, CommonProcess)
            assert _before_start <= cp.start_time <= _after_start

            cp.communicate(b'2 3 4 5 6')
            cp.join()

            _result = cp.process_result
            assert not _result.ok
            assert _result.signal_code == 9
            assert _result.exitcode == 0

    @pytest.mark.timeout(10.0)
    def test_common_process_rtle_pass(self):
        _before_start = time.time()
        with common_process(
                args="python3 -c \"print(sum([int(value) for value in input().split(' ')]));"
                     "import time;time.sleep(4.0);\"",
                resources=ResourceLimit(
                    max_real_time='20s',
                )
        ) as cp:
            _after_start = time.time()
            assert isinstance(cp, CommonProcess)
            assert _before_start <= cp.start_time <= _after_start

            _cresult = cp.communicate(b'2 3 4 5 6', wait=False)
            cp.join()
            assert cp.stdin == b'2 3 4 5 6'
            assert cp.stdout.decode().strip() == '20'
            assert cp.stderr.decode().strip() == ''

            assert _cresult is None

            cp.join()
            _result = cp.process_result
            assert _result is not None
            assert _result.ok
            assert _result.cpu_time < 0.5

    def test_common_process_direct_close(self):
        with common_process(args="echo 233") as cp:
            assert isinstance(cp, CommonProcess)

        _result = cp.process_result
        assert _result.ok

    def test_common_process_wtf(self):
        with pytest.raises(EnvironmentError):
            with common_process(args="what_the_fuck -a 1 -b 2"):
                pytest.fail('Should not reach here')

    def test_common_process_double_communicate(self):
        with common_process(args='cat') as cp:
            _stdout, _stderr = cp.communicate(b'123')
            assert _stdout.rstrip(b'\r\n') == b'123'
            assert _stderr.rstrip(b'\r\n') == b''

            with pytest.raises(RuntimeError):
                cp.communicate(b'')


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
