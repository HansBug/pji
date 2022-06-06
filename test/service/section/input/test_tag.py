import os

import pytest
from hbutils.testing import isolated_directory
from pysyslimit import FilePermission, SystemUser, SystemGroup

from pji.service.section.input.tag import TagFileInputTemplate
from pji.utils import FilePool


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestServiceSectionInputTag:
    def test_simple(self):
        tt = TagFileInputTemplate(
            tag='tag_x',
            local='./r.md',
            privilege='r--',
        )

        assert tt.tag == 'tag_x'
        assert tt.local == './r.md'
        assert tt.privilege == FilePermission.loads('400')

    def test_repr(self):
        assert repr(TagFileInputTemplate(
            tag='tag_x',
            local='./r.md',
            privilege='r--',
        )) == "<TagFileInputTemplate tag: 'tag_x', local: './r.md', privilege: 'r--------', condition: required>"

        assert repr(TagFileInputTemplate(
            tag='tag_x',
            local='./r.md',
            privilege='r--',
            condition='OPTIONAL',
        )) == "<TagFileInputTemplate tag: 'tag_x', local: './r.md', privilege: 'r--------', condition: optional>"

    def test_call_simple(self):
        tt = TagFileInputTemplate(
            tag='tag_x',
            local='./r.md',
            privilege='r--',
        )

        with FilePool({'tag_x': 'README.md'}) as pool, isolated_directory():
            fi = tt(workdir='.', pool=pool)

            assert fi.tag == 'tag_x'
            assert fi.local == os.path.abspath('r.md')
            assert fi.privilege == FilePermission.loads('400')

    def test_call_with_env(self):
        tt = TagFileInputTemplate(
            tag='tag_${T}_x',
            local='./${DIR}/r.md',
            privilege='r--',
        )

        with FilePool({'tag_x': 'README.md'}) as pool, isolated_directory():
            fi = tt(workdir='.', pool=pool, environ=dict(T='233', DIR='.'))

            assert fi.tag == 'tag_233_x'
            assert fi.local == os.path.abspath('r.md')
            assert fi.privilege == FilePermission.loads('400')

    def test_call_invalid(self):
        tt = TagFileInputTemplate(
            tag='tag_${T}_x',
            local='./${DIR}/r.md',
            privilege='r--',
        )

        with FilePool({'tag_x': 'README.md'}) as pool, isolated_directory():
            with pytest.raises(KeyError):
                tt(workdir='.', pool=pool, environ=dict(T='123/s', DIR='.'))
            with pytest.raises(ValueError):
                tt(workdir='.', pool=pool, environ=dict(T='123', DIR='..'))

    def test_call_execute(self):
        tt = TagFileInputTemplate(
            tag='tag_x',
            local='./r.md',
            privilege='r--',
        )
        original_path = os.path.abspath('.')

        with FilePool({'tag_x': 'README.md'}) as pool, isolated_directory():
            fi = tt(workdir='.', pool=pool)
            _is_completed = False

            def _complete():
                nonlocal _is_completed
                _is_completed = True

            fi(input_complete=_complete)
            assert _is_completed

            assert os.path.exists('r.md')
            assert FilePermission.load_from_file('r.md') == FilePermission.loads('400')
            with open(os.path.join(original_path, 'README.md'), 'rb') as of, open('r.md', 'rb') as tf:
                assert of.read() == tf.read()

    def test_call_execute_with_identification(self):
        tt = TagFileInputTemplate(
            tag='tag_x',
            local='./r.md',
            privilege='r--',
            identification='nobody',
        )
        original_path = os.path.abspath('.')

        with FilePool({'tag_x': 'README.md'}) as pool, isolated_directory():
            fi = tt(workdir='.', pool=pool)
            _is_completed = False

            def _complete():
                nonlocal _is_completed
                _is_completed = True

            fi(input_complete=_complete)
            assert _is_completed

            assert os.path.exists('r.md')
            assert FilePermission.load_from_file('r.md') == FilePermission.loads('400')
            assert SystemUser.load_from_file('r.md') == SystemUser.loads('nobody')
            assert SystemGroup.load_from_file('r.md') == SystemGroup.loads('nogroup')
            with open(os.path.join(original_path, 'README.md'), 'rb') as of, open('r.md', 'rb') as tf:
                assert of.read() == tf.read()

    def test_tag_failed(self):
        tt = TagFileInputTemplate(
            tag='tag_xxxxxxxxxxxxxxxxxxxxxxxxxxx',
            local='./r.md',
            privilege='r--',
        )

        with FilePool({'tag_x': 'README.md'}) as pool, isolated_directory():
            fi = tt(workdir='.', pool=pool)
            _is_completed = False

            def _complete():
                nonlocal _is_completed
                _is_completed = True

            with pytest.raises(KeyError):
                fi(input_complete=_complete)
            assert not _is_completed

            assert not os.path.exists('r.md')

    def test_tag_skipped(self):
        tt = TagFileInputTemplate(
            tag='tag_xxxxxxxxxxxxxxxxxxxxxxxxxxx',
            local='./r.md',
            privilege='r--',
            condition='optional',
        )

        with FilePool({'tag_x': 'README.md'}) as pool, isolated_directory():
            fi = tt(workdir='.', pool=pool)
            _is_completed, _is_skipped = False, False

            def _complete():
                nonlocal _is_completed
                _is_completed = True

            def _skip():
                nonlocal _is_skipped
                _is_skipped = True

            fi(input_complete=_complete, input_skip=_skip)
            assert not _is_completed
            assert _is_skipped

            assert not os.path.exists('r.md')
