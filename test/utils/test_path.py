import os
import shutil
import tempfile

import pytest
from pysystem import FileAuthority, SystemUser, SystemGroup

from pji.utils import is_absolute_path, is_relative_path, is_inner_relative_path, makedirs


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

    def test_makedirs_without_privilege_and_user(self):
        with tempfile.TemporaryDirectory() as td:
            _target_dir = os.path.join(td, '1', '2', '..', '3', '4')
            makedirs(_target_dir)

            _target_dir = os.path.normpath(_target_dir)
            assert os.path.exists(_target_dir)
            assert os.path.isdir(_target_dir)

    def test_makedirs(self):
        with tempfile.TemporaryDirectory() as td:
            _target_dir = os.path.join(td, '1', '2', '..', '3', '4')
            makedirs(_target_dir, '356', 'nobody', 'nogroup')

            _target_dir = os.path.normpath(_target_dir)
            assert os.path.exists(_target_dir)
            assert os.path.isdir(_target_dir)
            assert FileAuthority.load_from_file(_target_dir) == FileAuthority.loads('-wxr-xrw-')
            assert SystemUser.load_from_file(_target_dir) == SystemUser.loads('nobody')
            assert SystemGroup.load_from_file(_target_dir) == SystemGroup.loads('nogroup')
            assert FileAuthority.load_from_file(os.path.join(_target_dir, '..')) == FileAuthority.loads('-wxr-xrw-')
            assert SystemUser.load_from_file(os.path.join(_target_dir, '..')) == SystemUser.loads('nobody')
            assert SystemGroup.load_from_file(os.path.join(_target_dir, '..')) == SystemGroup.loads('nogroup')
            assert FileAuthority.load_from_file(os.path.join(_target_dir, '../..')) == FileAuthority.loads('-wxr-xrw-')
            assert SystemUser.load_from_file(os.path.join(_target_dir, '../..')) == SystemUser.loads('nobody')
            assert SystemGroup.load_from_file(os.path.join(_target_dir, '../..')) == SystemGroup.loads('nogroup')

    def test_makedirs_invalid(self):
        with tempfile.TemporaryDirectory() as td:
            shutil.copyfile('README.md', os.path.join(td, 'r'))
            with pytest.raises(NotADirectoryError):
                makedirs(os.path.join(td, 'r', '1', '2'), '356', 'nobody', 'nogroup')


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
