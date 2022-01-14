import pytest

from pji.utils import ValueProxy


@pytest.mark.unittest
class TestUtilsValue:
    def test_value_proxy_init(self):
        value = ValueProxy()
        assert value.value is None

        value = ValueProxy(233)
        assert value.value == 233

    def test_value_proxy_set(self):
        value = ValueProxy()
        value.value = 233
        assert value.value == 233

        value.value = -27
        assert value.value == -27
