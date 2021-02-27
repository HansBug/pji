import os

import pytest
from bitmath import MiB, GB

from pji.utils import size_to_bytes, time_to_duration, size_to_bytes_str, time_to_delta_str


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

    def test_size_to_bytes_str(self):
        assert size_to_bytes_str(233) == '233.0 Byte'
        assert size_to_bytes_str(2.3) == '2.3 Byte'
        assert size_to_bytes_str('200000kib') == '195.3125 MiB'

    def test_time_to_duration(self):
        assert time_to_duration(2) == 2
        assert time_to_duration(2.3) == 2.3
        assert time_to_duration('2s') == 2
        assert time_to_duration('2min5s') == 125
        assert time_to_duration('1h5.5s') == 3605.5

    def test_time_to_duration_invalid(self):
        with pytest.raises(TypeError):
            time_to_duration([1, 2, 3])

    def test_time_to_delta_str(self):
        assert time_to_delta_str(2) == '0:00:02'
        assert time_to_delta_str(2.3) == '0:00:02.300000'
        assert time_to_delta_str('2s') == '0:00:02'
        assert time_to_delta_str('2min5s') == '0:02:05'
        assert time_to_delta_str('2min170s') == '0:04:50'
        assert time_to_delta_str('1h5.5s') == '1:00:05.500000'


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
