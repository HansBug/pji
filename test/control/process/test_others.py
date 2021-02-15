import os

import pytest
import where

from pji.control import common_process, ExecutorException


@pytest.mark.unittest
class TestControlProcessOthers:
    def test_user_change(self):
        cp = common_process(
            args="python3 -c 'import os, grp, getpass;print(getpass.getuser(), grp.getgrgid(os.getgid()).gr_name)'",
            user='nobody',
        )

        cp.communicate()
        cp.join()
        assert cp.stdout.rstrip(b'\r\n') == b'nobody nogroup'
        assert cp.stderr.rstrip(b'\r\n') == b''

        _result = cp.result
        assert _result is not None
        assert _result.ok

    def test_group_change(self):
        cp = common_process(
            args="python3 -c 'import os, grp, getpass;print(getpass.getuser(), grp.getgrgid(os.getgid()).gr_name)'",
            group='nogroup',
        )

        cp.communicate()
        cp.join()
        assert cp.stdout.rstrip(b'\r\n') == b'root nogroup'
        assert cp.stderr.rstrip(b'\r\n') == b''

        _result = cp.result
        assert _result is not None
        assert _result.ok

    @pytest.mark.timeout(5.0)
    def test_dict_resource(self):
        with common_process(
                args="python3 -c \"while True: pass\"",
                resources=dict(
                    max_real_time='2s',
                )
        ) as cp:
            pass

        _result = cp.result
        assert _result is not None

    def test_invalid_resource(self):
        with pytest.raises(TypeError):
            with common_process(
                    args="python3 -c \"while True: pass\"",
                    resources=[1, 2, 3],
            ):
                pytest.fail('Should not reach here.')

    def test_no_such_cwd(self):
        with pytest.raises(FileNotFoundError):
            with common_process(
                    args='echo 233',
                    cwd='/path/not/exist/wtf',
            ):
                pytest.fail('Should not reach here.')

    def test_not_a_directory(self):
        file = where.first('sh') or where.first('python') or where.first('python3')
        with pytest.raises(NotADirectoryError):
            with common_process(
                    args='echo 233',
                    cwd=file,
            ):
                pytest.fail('Should not reach here.')

    def test_real_time_limit_key(self):
        with pytest.raises(KeyError):
            with common_process(
                    args='echo 233',
                    real_time_limit=4.0,
            ):
                pytest.fail('Should not reach here.')

    @pytest.mark.timeout(5.0)
    def test_exception_in_executor(self):
        def _preexec_fn():
            raise RuntimeError

        with pytest.raises(ExecutorException) as ei:
            with common_process(
                    args="echo 233",
                    preexec_fn=_preexec_fn,
                    resources=dict(
                        max_real_time='2s',
                    )
            ):
                pytest.fail('Should not reach here.')

        err = ei.value
        assert isinstance(err, ExecutorException)
        assert isinstance(err.exception, RuntimeError)


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
