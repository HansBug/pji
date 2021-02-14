import os

import pytest

from pji.control import common_process


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


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
