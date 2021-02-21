import os
import tempfile

import pytest
from pysystem import FileAuthority

from pji.service.section.input import CopyFileInputTemplate


@pytest.mark.unittest
class TestServiceSectionInputCopy:
    def test_template(self):
        cf = CopyFileInputTemplate(
            file='README.md',
            local='./r.md',
            privilege='r--'
        )

        assert cf.file == 'README.md'
        assert cf.local == './r.md'
        assert cf.privilege == FileAuthority.loads('r--------')

    def test_template_repr(self):
        cf = CopyFileInputTemplate(
            file='README.md',
            local='./r.md',
            privilege='r--'
        )

        assert repr(cf) == "<CopyFileInputTemplate file: 'README.md', local: './r.md', privilege: 'r--------'>"

    def test_template_invalid(self):
        with pytest.raises(ValueError):
            CopyFileInputTemplate(
                file='README.md',
                local='../r.md',
                privilege='r--'
            )
        with pytest.raises(ValueError):
            CopyFileInputTemplate(
                file='README.md',
                local='.',
                privilege='r--'
            )

    def test_template_call_and_copy(self):
        cf = CopyFileInputTemplate(
            file='README.md',
            local='./r.md',
            privilege='r--'
        )
        with tempfile.TemporaryDirectory() as fd:
            c = cf(os.curdir, fd)

            assert c.file == 'README.md'
            assert c.local == os.path.normpath(os.path.join(fd, 'r.md'))
            assert c.privilege == FileAuthority.loads('r--------')

    def test_copy_repr(self):
        cf = CopyFileInputTemplate(
            file='README.md',
            local='./r.md',
            privilege='r--'
        )
        with tempfile.TemporaryDirectory() as fd:
            c = cf(os.curdir, fd)

            assert repr(c) == "<CopyFileInput file: 'README.md', " \
                              "local: '{fd}/r.md', privilege: 'r--------'>".format(fd=fd)

    def test_copy_call_with_short_privilege(self):
        cf = CopyFileInputTemplate(
            file='README.md',
            local='./r.md',
            privilege='r--'
        )
        with tempfile.TemporaryDirectory() as fd:
            c = cf(os.curdir, fd)
            c()

            _target_file = os.path.normpath(os.path.join(fd, 'r.md'))
            assert os.path.exists(_target_file)
            assert FileAuthority.load_from_file(_target_file) == FileAuthority.loads('r--------')
            with open('README.md', 'rb') as of, \
                    open(_target_file, 'rb') as tf:
                assert of.read() == tf.read()

    def test_copy_call_with_full_privilege(self):
        cf = CopyFileInputTemplate(
            file='README.md',
            local='./r.md',
            privilege='777'
        )
        with tempfile.TemporaryDirectory() as fd:
            c = cf(os.curdir, fd)
            c()

            _target_file = os.path.normpath(os.path.join(fd, 'r.md'))
            assert os.path.exists(_target_file)
            assert FileAuthority.load_from_file(_target_file) == FileAuthority.loads('rwxrwxrwx')
            with open('README.md', 'rb') as of, \
                    open(_target_file, 'rb') as tf:
                assert of.read() == tf.read()

    def test_copy_call_without_privilege(self):
        cf = CopyFileInputTemplate(
            file='README.md',
            local='./r.md',
        )
        with tempfile.TemporaryDirectory() as fd:
            c = cf(os.curdir, fd)
            c()

            _target_file = os.path.normpath(os.path.join(fd, 'r.md'))
            with open('README.md', 'rb') as of, \
                    open(_target_file, 'rb') as tf:
                assert of.read() == tf.read()

    def test_copy_call_with_env(self):
        cf = CopyFileInputTemplate(
            file='README.md',
            local='./${DIR}/r.md',
            privilege='r--'
        )
        with tempfile.TemporaryDirectory() as fd:
            c = cf(os.curdir, fd, dict(DIR='123'))
            c()

            _target_file = os.path.normpath(os.path.join(fd, '123', 'r.md'))
            assert os.path.exists(_target_file)
            assert FileAuthority.load_from_file(_target_file) == FileAuthority.loads('r--------')
            with open('README.md', 'rb') as of, \
                    open(_target_file, 'rb') as tf:
                assert of.read() == tf.read()

    def test_copy_call_dir(self):
        cf = CopyFileInputTemplate(
            file='pji',
            local='pinit.py',
            privilege='rw-'
        )
        with tempfile.TemporaryDirectory() as fd:
            c = cf(os.curdir, fd)
            c()

            _target_dir = os.path.normpath(os.path.join(fd, 'pinit.py'))
            assert os.path.exists(_target_dir)
            assert FileAuthority.load_from_file(os.path.join(_target_dir, '__init__.py')) == FileAuthority.loads(
                'rw-------')
            with open(os.path.normpath(os.path.join('pji', '__init__.py')), 'rb') as of, \
                    open(os.path.normpath(os.path.join(_target_dir, '__init__.py')), 'rb') as tf:
                assert of.read() == tf.read()


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
