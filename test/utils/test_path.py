import os

import pytest

from pji.utils import is_absolute_path, is_relative_path, is_inner_relative_path


@pytest.mark.unittest
class TestUtilsPath:
    def test_is_absolute(self):
        assert is_absolute_path('/')
        assert is_absolute_path('/root/1/2/3')
        assert not is_absolute_path('.')
        assert not is_absolute_path('../root/1/2/3')

    def test_is_relative(self):
        assert not is_relative_path('/')
        assert not is_relative_path('/root/1/2/3')
        assert is_relative_path('.')
        assert is_relative_path('../root/1/2/3')

    def test_is_inner_relative(self):
        assert not is_inner_relative_path('/')
        assert not is_inner_relative_path('/root/1/2/3')
        assert is_inner_relative_path('.')
        assert not is_inner_relative_path('.', allow_root=False)
        assert not is_inner_relative_path('..')
        assert not is_inner_relative_path('../1/..')


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
