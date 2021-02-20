import os

import pytest


@pytest.mark.unittest
class TestUtilsPath:
    def test_is_absolute(self):
        pass


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
