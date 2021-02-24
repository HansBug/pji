import os

import pytest


@pytest.mark.unittest
class TestServiceTaskTask:
    def test_task_simple(self):
        pass


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
