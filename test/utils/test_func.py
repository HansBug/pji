import pytest

from pji.utils import wrap_empty


@pytest.mark.unittest
class TestUtilsFunc:
    def test_wrap_empty(self):
        assert wrap_empty(lambda x: x + 1)(2) == 3
        assert wrap_empty(None)(2) is None
        assert wrap_empty(lambda x: x + 1)(2, 3) == 3
        assert wrap_empty(list)('ksdjfl') == ['k', 's', 'd', 'j', 'f', 'l']
