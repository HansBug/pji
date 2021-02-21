import os
import tempfile

import pytest
from pysystem import FileAuthority

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
        assert tt.privilege == FileAuthority.loads('400')

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
            assert fi.privilege == FileAuthority.loads('400')

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
            assert fi.privilege == FileAuthority.loads('400')

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
            assert FileAuthority.load_from_file(_target_path) == FileAuthority.loads('400')
            with open('README.md', 'rb') as of, \
                    open(_target_path, 'rb') as tf:
                assert of.read() == tf.read()


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
