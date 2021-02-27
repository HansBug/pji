import os

import pytest

from pji.service.command import CommandMode


@pytest.mark.unittest
class TestServiceCommandBase:
    def test_mode_loads(self):
        assert CommandMode.loads(CommandMode.COMMON) == CommandMode.COMMON
        assert CommandMode.loads(CommandMode.TIMING) == CommandMode.TIMING
        assert CommandMode.loads(CommandMode.MUTUAL) == CommandMode.MUTUAL
        assert CommandMode.loads(1) == CommandMode.COMMON
        assert CommandMode.loads(2) == CommandMode.TIMING
        assert CommandMode.loads(3) == CommandMode.MUTUAL
        assert CommandMode.loads('common') == CommandMode.COMMON
        assert CommandMode.loads('Timing') == CommandMode.TIMING
        assert CommandMode.loads('MUTUAL') == CommandMode.MUTUAL

    def test_mode_loads_invalid(self):
        with pytest.raises(KeyError):
            CommandMode.loads('common_')
        with pytest.raises(ValueError):
            CommandMode.loads(-1)
        with pytest.raises(TypeError):
            CommandMode.loads([])


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
