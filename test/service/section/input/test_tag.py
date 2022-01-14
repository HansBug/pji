import os
import tempfile

import pytest
from pysyslimit import FilePermission, SystemUser, SystemGroup

from pji.service.section.input.tag import TagFileInputTemplate
from pji.utils import FilePool


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
        tt = TagFileInputTemplate(
            tag='tag_x',
            local='./r.md',
            privilege='r--',
        )

        assert repr(tt) == "<TagFileInputTemplate tag: 'tag_x', local: './r.md', privilege: 'r--------'>"

    def test_call_simple(self):
        tt = TagFileInputTemplate(
            tag='tag_x',
            local='./r.md',
            privilege='r--',
        )

        with FilePool({'tag_x': 'README.md'}) as pool, \
                tempfile.TemporaryDirectory() as td:
            fi = tt(workdir=td, pool=pool)

            assert fi.tag == 'tag_x'
            assert fi.local == os.path.normpath(os.path.join(td, 'r.md'))
            assert fi.privilege == FilePermission.loads('400')

    def test_call_with_env(self):
        tt = TagFileInputTemplate(
            tag='tag_${T}_x',
            local='./${DIR}/r.md',
            privilege='r--',
        )

        with FilePool({'tag_x': 'README.md'}) as pool, \
                tempfile.TemporaryDirectory() as td:
            fi = tt(workdir=td, pool=pool, environ=dict(T='233', DIR='.'))

            assert fi.tag == 'tag_233_x'
            assert fi.local == os.path.normpath(os.path.join(td, 'r.md'))
            assert fi.privilege == FilePermission.loads('400')

    def test_call_invalid(self):
        tt = TagFileInputTemplate(
            tag='tag_${T}_x',
            local='./${DIR}/r.md',
            privilege='r--',
        )

        with FilePool({'tag_x': 'README.md'}) as pool, \
                tempfile.TemporaryDirectory() as td:
            with pytest.raises(KeyError):
                tt(workdir=td, pool=pool, environ=dict(T='123/s', DIR='.'))
            with pytest.raises(ValueError):
                tt(workdir=td, pool=pool, environ=dict(T='123', DIR='..'))

    def test_call_execute(self):
        tt = TagFileInputTemplate(
            tag='tag_x',
            local='./r.md',
            privilege='r--',
        )

        with FilePool({'tag_x': 'README.md'}) as pool, \
                tempfile.TemporaryDirectory() as td:
            fi = tt(workdir=td, pool=pool)
            fi()

            _target_path = os.path.normpath(os.path.join(td, 'r.md'))
            assert os.path.exists(_target_path)
            assert FilePermission.load_from_file(_target_path) == FilePermission.loads('400')
            with open('README.md', 'rb') as of, \
                    open(_target_path, 'rb') as tf:
                assert of.read() == tf.read()

    def test_call_execute_with_identification(self):
        tt = TagFileInputTemplate(
            tag='tag_x',
            local='./r.md',
            privilege='r--',
            identification='nobody',
        )

        with FilePool({'tag_x': 'README.md'}) as pool, \
                tempfile.TemporaryDirectory() as td:
            fi = tt(workdir=td, pool=pool)
            fi()

            _target_path = os.path.normpath(os.path.join(td, 'r.md'))
            assert os.path.exists(_target_path)
            assert FilePermission.load_from_file(_target_path) == FilePermission.loads('400')
            assert SystemUser.load_from_file(_target_path) == SystemUser.loads('nobody')
            assert SystemGroup.load_from_file(_target_path) == SystemGroup.loads('nogroup')
            with open('README.md', 'rb') as of, \
                    open(_target_path, 'rb') as tf:
                assert of.read() == tf.read()
