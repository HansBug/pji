import os

import pytest
from hbutils.testing import isolated_directory
from pysyslimit import FilePermission, SystemUser, SystemGroup

from pji.service.section.input import CopyFileInputTemplate, CopyFileInput


# noinspection DuplicatedCode
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
        assert cf.privilege == FilePermission.loads('r--------')

    def test_template_repr(self):
        assert repr(CopyFileInputTemplate(
            file='README.md',
            local='./r.md',
            privilege='r--'
        )) == "<CopyFileInputTemplate file: 'README.md', local: './r.md', privilege: 'r--------', condition: required>"

        assert repr(CopyFileInputTemplate(
            file='README.md',
            local='./r.md',
            privilege='r--',
            condition='optional',
        )) == "<CopyFileInputTemplate file: 'README.md', local: './r.md', privilege: 'r--------', condition: optional>"

    def test_template_call_and_copy(self):
        cf = CopyFileInputTemplate(
            file='README.md',
            local='./r.md',
            privilege='r--'
        )
        original_path = os.path.abspath('.')

        with isolated_directory():
            c = cf(original_path, '.')

            assert c.file == os.path.join(original_path, 'README.md')
            assert c.local == os.path.abspath('r.md')
            assert c.privilege == FilePermission.loads('r--------')

    def test_template_call_invalid(self):
        cf = CopyFileInputTemplate(
            file='README.md',
            local='./${DIR}/r.md',
            privilege='r--'
        )
        original_path = os.path.abspath('.')

        with isolated_directory():
            with pytest.raises(ValueError):
                cf(original_path, '.', None, dict(DIR='..'))

    def test_copy_repr(self):
        cf = CopyFileInputTemplate(
            file='README.md',
            local='./r.md',
            privilege='r--',
            condition='optional',
        )
        original_path = os.path.abspath('.')

        with isolated_directory():
            c = cf(original_path, '.')

            assert repr(c) == f"<CopyFileInput file: '{os.path.join(original_path, 'README.md')}', " \
                              f"local: '{os.path.abspath('r.md')}', privilege: 'r--------', " \
                              f"condition: optional>"

    def test_copy_call_with_short_privilege(self):
        cf = CopyFileInputTemplate(
            file='README.md',
            local='./r.md',
            privilege='r--'
        )
        original_path = os.path.abspath('.')

        with isolated_directory():
            c = cf(original_path, '.')
            _is_completed = False

            # noinspection PyUnusedLocal
            def _complete(inp: CopyFileInput):
                nonlocal _is_completed
                _is_completed = True

            c(input_complete=_complete)
            assert _is_completed

            assert os.path.exists('r.md')
            assert FilePermission.load_from_file('r.md') == FilePermission.loads('r--------')
            with open(os.path.join(original_path, 'README.md'), 'rb') as of, open('r.md', 'rb') as tf:
                assert of.read() == tf.read()

    def test_copy_call_with_full_privilege(self):
        cf = CopyFileInputTemplate(
            file='README.md',
            local='./r.md',
            privilege='777'
        )
        original_path = os.path.abspath('.')

        with isolated_directory():
            c = cf(original_path, '.')
            _is_completed = False

            def _complete():
                nonlocal _is_completed
                _is_completed = True

            c(input_complete=_complete)
            assert _is_completed

            assert os.path.exists('r.md')
            assert FilePermission.load_from_file('r.md') == FilePermission.loads('rwxrwxrwx')
            with open(os.path.join(original_path, 'README.md'), 'rb') as of, open('r.md', 'rb') as tf:
                assert of.read() == tf.read()

    def test_copy_call_with_identification(self):
        cf = CopyFileInputTemplate(
            file='README.md',
            local='./r.md',
            privilege='r--',
            identification='nobody',
        )
        original_path = os.path.abspath('.')

        with isolated_directory():
            c = cf(original_path, '.')
            _is_completed = False

            def _complete():
                nonlocal _is_completed
                _is_completed = True

            c(input_complete=_complete)
            assert _is_completed

            assert os.path.exists('r.md')
            assert FilePermission.load_from_file('r.md') == FilePermission.loads('r--------')
            assert SystemUser.load_from_file('r.md') == SystemUser.loads('nobody')
            assert SystemGroup.load_from_file('r.md') == SystemGroup.loads('nogroup')
            with open(os.path.join(original_path, 'README.md'), 'rb') as of, open('r.md', 'rb') as tf:
                assert of.read() == tf.read()

    def test_copy_call_without_privilege(self):
        cf = CopyFileInputTemplate(
            file='README.md',
            local='./r.md',
        )
        original_path = os.path.abspath('.')

        with isolated_directory():
            c = cf(original_path, '.')
            _is_completed = False

            def _complete():
                nonlocal _is_completed
                _is_completed = True

            c(input_complete=_complete)
            assert _is_completed

            with open(os.path.join(original_path, 'README.md'), 'rb') as of, open('r.md', 'rb') as tf:
                assert of.read() == tf.read()

    def test_copy_call_with_env(self):
        cf = CopyFileInputTemplate(
            file='README.md',
            local='./${DIR}/r.md',
            privilege='r--'
        )
        original_path = os.path.abspath('.')

        with isolated_directory():
            c = cf(original_path, '.', 'nobody', dict(DIR='123'))
            _is_completed = False

            def _complete():
                nonlocal _is_completed
                _is_completed = True

            c(input_complete=_complete)
            assert _is_completed

            assert os.path.exists('123/r.md')
            assert FilePermission.load_from_file('123/r.md') == FilePermission.loads('r--------')
            assert SystemUser.load_from_file('123/r.md') == SystemUser.loads('nobody')
            assert SystemGroup.load_from_file('123/r.md') == SystemGroup.loads('nogroup')
            with open(os.path.join(original_path, 'README.md'), 'rb') as of, open('123/r.md', 'rb') as tf:
                assert of.read() == tf.read()

    def test_copy_call_dir(self):
        cf = CopyFileInputTemplate(
            file='pji',
            local='pinit.py',
            privilege='rw-'
        )
        original_path = os.path.abspath('.')

        with isolated_directory():
            c = cf(original_path, '.')
            _is_completed = False

            def _complete():
                nonlocal _is_completed
                _is_completed = True

            c(input_complete=_complete)
            assert _is_completed

            assert os.path.exists('pinit.py')
            assert FilePermission.load_from_file(os.path.join('pinit.py', '__init__.py')) == \
                   FilePermission.loads('rw-------')
            with open(os.path.join(original_path, 'pji', '__init__.py'), 'rb') as of, \
                    open(os.path.join('pinit.py', '__init__.py'), 'rb') as tf:
                assert of.read() == tf.read()

    def test_copy_failed(self):
        cf = CopyFileInputTemplate(
            file='pjiuw89ertu92384hrfijhdweskf',
            local='pinit.py',
            privilege='rw-'
        )
        original_path = os.path.abspath('.')

        with isolated_directory():
            c = cf(original_path, '.')
            _is_completed = False

            def _complete():
                nonlocal _is_completed
                _is_completed = True

            with pytest.raises(FileNotFoundError):
                c(input_complete=_complete)
            assert not _is_completed

    def test_copy_skip(self):
        cf = CopyFileInputTemplate(
            file='pjiuw89ertu92384hrfijhdweskf',
            local='pinit.py',
            privilege='rw-',
            condition='optional',
        )
        original_path = os.path.abspath('.')

        with isolated_directory():
            c = cf(original_path, '.')
            _is_completed, _is_skipped = False, False

            def _complete():
                nonlocal _is_completed
                _is_completed = True

            def _skip():
                nonlocal _is_skipped
                _is_skipped = True

            c(input_complete=_complete, input_skip=_skip)
            assert not _is_completed
            assert _is_skipped
            assert not os.path.exists('pinit.py')
