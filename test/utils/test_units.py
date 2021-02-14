import os

import pytest
from bitmath import MiB, GB

from pji.utils import size_to_bytes


@pytest.mark.unittest
class TestUtilsUnits:
    def test_size_to_bytes(self):
        assert size_to_bytes(233) == 233
        assert size_to_bytes('2KB') == 2000
        assert size_to_bytes('2KiB') == 2048
        assert size_to_bytes('2kb') == 2000
        assert size_to_bytes('2kib') == 2048
        assert size_to_bytes(MiB(512)) == 512 << 20
        assert size_to_bytes(GB(3)) == 3 * 10 ** 9

    def test_size_to_bytes_invalid(self):
        with pytest.raises(TypeError):
            assert size_to_bytes(20.3)
        with pytest.raises(TypeError):
            assert size_to_bytes([1, 2, 3])


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
