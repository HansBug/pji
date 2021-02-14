import os

import pytest

from pji.utils import allow_none


@pytest.mark.unittest
class TestUtilsDecorator:
    def test_allow_none(self):
        _demo_func = allow_none(str)
        assert _demo_func(1) == '1'
        assert _demo_func('sdfkljksdko') == 'sdfkljksdko'
        assert _demo_func(None) is None


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
