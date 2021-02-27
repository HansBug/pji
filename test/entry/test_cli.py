import os

import pytest


@pytest.mark.unittest
class TestEntryCli:
    def test_simple(self):
        pass


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
