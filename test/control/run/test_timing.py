import os

import pytest


@pytest.mark.unittest
class TestControlRunTiming:
    def test_nothing(self):
        pass


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
