import os

import pytest

from pji.utils import args_split


@pytest.mark.unittest
class TestUtilsArgs:
    def test_args_split(self):
        assert args_split('python test_main.py') == ['python', 'test_main.py']
        assert args_split('python "test_main.py"') == ['python', 'test_main.py']
        assert args_split(['python', 'test_main.py']) == ['python', 'test_main.py']


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
