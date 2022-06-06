import os

import pytest
from hbutils.testing import isolated_directory

from pji.service.section.input.link import LinkFileInputTemplate


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestServiceSectionInputLink:
    def test_template(self):
        lf = LinkFileInputTemplate(
            file='README.md',
            local='./r.md',
        )

        assert lf.file == 'README.md'
        assert lf.local == './r.md'

    def test_template_repr(self):
        assert repr(LinkFileInputTemplate(
            file='README.md',
            local='./r.md',
        )) == "<LinkFileInputTemplate file: 'README.md', local: './r.md', condition: required>"

        assert repr(LinkFileInputTemplate(
            file='README.md',
            local='./r.md',
            condition='optional',
        )) == "<LinkFileInputTemplate file: 'README.md', local: './r.md', condition: optional>"

    def test_template_call_and_link(self):
        lf = LinkFileInputTemplate(
            file='README.md',
            local='./r.md',
        )
        original_path = os.path.abspath('.')

        with isolated_directory():
            ln = lf(original_path, '.')

            assert ln.file == os.path.join(original_path, 'README.md')
            assert ln.local == os.path.abspath('r.md')

    def test_template_call_invalid(self):
        lf = LinkFileInputTemplate(
            file='README.md',
            local='./${DIR}/r.md',
        )
        original_path = os.path.abspath('.')

        with isolated_directory():
            with pytest.raises(ValueError):
                lf(original_path, '.', dict(DIR='..'))
            with pytest.raises(KeyError):
                lf(original_path, '.', None)

    def test_link_repr(self):
        lf = LinkFileInputTemplate(
            file='README.md',
            local='./r.md',
            condition='optional',
        )
        original_path = os.path.abspath('.')

        with isolated_directory():
            ln = lf(original_path, '.')

            assert repr(ln) == f"<LinkFileInput file: '{os.path.join(original_path, 'README.md')}', " \
                               f"local: '{os.path.abspath('r.md')}', condition: optional>"

    def test_link_call(self):
        lf = LinkFileInputTemplate(
            file='README.md',
            local='./r.md',
        )
        original_path = os.path.abspath('.')

        with isolated_directory():
            ln = lf(original_path, '.')
            _is_completed = False

            def _complete():
                nonlocal _is_completed
                _is_completed = True

            ln(input_complete=_complete)
            assert _is_completed

            assert os.path.exists('r.md')
            assert os.path.islink('r.md')
            with open(os.path.join(original_path, 'README.md'), 'rb') as of, open('r.md', 'rb') as tf:
                assert of.read() == tf.read()

    def test_link_call_dir(self):
        lf = LinkFileInputTemplate(
            file='pji',
            local='pinit.py',
        )
        original_path = os.path.abspath('.')

        with isolated_directory():
            ln = lf(original_path, '.')
            _is_completed = False

            def _complete():
                nonlocal _is_completed
                _is_completed = True

            ln(input_complete=_complete)
            assert _is_completed

            assert os.path.exists('pinit.py')
            assert os.path.islink('pinit.py')
            with open(os.path.join(original_path, 'pji', '__init__.py'), 'rb') as of, \
                    open(os.path.join('pinit.py', '__init__.py'), 'rb') as tf:
                assert of.read() == tf.read()

    def test_link_failed(self):
        lf = LinkFileInputTemplate(
            file='README.mdxxxxxxxxxxxxxxx',
            local='./r.md',
        )
        original_path = os.path.abspath('.')

        with isolated_directory():
            ln = lf(original_path, '.')
            _is_completed = False

            def _complete():
                nonlocal _is_completed
                _is_completed = True

            with pytest.raises(FileNotFoundError):
                ln(input_complete=_complete)
            assert not _is_completed
            assert not os.path.exists('r.md')

    def test_link_skipped(self):
        lf = LinkFileInputTemplate(
            file='README.mdxxxxxxxxxxxxxxx',
            local='./r.md',
            condition='optional',
        )
        original_path = os.path.abspath('.')

        with isolated_directory():
            ln = lf(original_path, '.')
            _is_completed, _is_skipped = False, False

            def _complete():
                nonlocal _is_completed
                _is_completed = True

            def _skip():
                nonlocal _is_skipped
                _is_skipped = True

            ln(input_complete=_complete, input_skip=_skip)
            assert not _is_completed
            assert _is_skipped
            assert not os.path.exists('r.md')
