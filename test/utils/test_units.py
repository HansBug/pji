import os

import pytest
from bitmath import MiB, GB

from pji.utils import size_to_bytes, time_to_duration


@pytest.mark.unittest
class TestUtilsUnits:
    def test_size_to_bytes(self):
        assert size_to_bytes(233) == 233
        assert size_to_bytes(20.3) == 20.3
        assert size_to_bytes('2KB') == 2000
        assert size_to_bytes('2KiB') == 2048
        assert size_to_bytes('2kb') == 2000
        assert size_to_bytes('2kib') == 2048
        assert size_to_bytes(MiB(512)) == 512 << 20
        assert size_to_bytes(GB(3)) == 3 * 10 ** 9

    def test_size_to_bytes_invalid(self):
        with pytest.raises(TypeError):
            assert size_to_bytes([1, 2, 3])

    def test_time_to_duration(self):
        assert time_to_duration(2) == 2
        assert time_to_duration(2.3) == 2.3
        assert time_to_duration('2s') == 2
        assert time_to_duration('2min5s') == 125
        assert time_to_duration('1h5.5s') == 3605.5

    def test_time_to_duration_invalid(self):
        with pytest.raises(TypeError):
            time_to_duration([1, 2, 3])


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
