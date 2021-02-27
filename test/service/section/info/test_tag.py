import os

import pytest

from pji.service.section.info.tag import TagSectionInfoTemplate
from pji.utils import FilePool


@pytest.mark.unittest
class TestServiceSectionInfoTag:
    def test_simple(self):
        tt = TagSectionInfoTemplate(
            tag='tag_${NO}_x',
        )

        assert tt.tag == 'tag_${NO}_x'
        assert tt.file is None
        assert repr(tt) == "<TagSectionInfoTemplate tag: 'tag_${NO}_x'>"

    def test_simple_with_file(self):
        tt = TagSectionInfoTemplate(
            tag='tag_${NO}_x',
            file='./r.md'
        )

        assert tt.tag == 'tag_${NO}_x'
        assert tt.file == './r.md'
        assert repr(tt) == "<TagSectionInfoTemplate tag: 'tag_${NO}_x', file: './r.md'>"

    def test_call(self):
        tt = TagSectionInfoTemplate(
            tag='tag_${NO}_x',
        )

        with FilePool() as pool:
            t = tt(pool=pool, environ=dict(NO='233'))

            assert t.tag == 'tag_233_x'
            assert t.file is None

    def test_call_with_file(self):
        tt = TagSectionInfoTemplate(
            tag='tag_${NO}_x',
            file='./r${NO}.md'
        )

        with FilePool() as pool:
            t = tt(pool=pool, environ=dict(NO='233'))

            assert t.tag == 'tag_233_x'
            assert t.file == 'r233.md'

    def test_call_invalid(self):
        tt = TagSectionInfoTemplate(
            tag='tag_${NOX}_x',
            file='./r${NOD}.md'
        )

        with FilePool() as pool:
            with pytest.raises(KeyError):
                tt(pool=pool, environ=dict(NOX='233.', NOD=''))
            with pytest.raises(ValueError):
                tt(pool=pool, environ=dict(NOX='233', NOD='/../../x'))

    def test_call_execute(self):
        tt = TagSectionInfoTemplate(
            tag='tag_${NOX}_x',
        )

        with FilePool({'tag_233_x': 'README.md'}) as pool:
            t = tt(pool=pool, environ=dict(NOX='233'))

            with open('README.md', 'r') as of:
                assert t() == (True, of.read())

    def test_call_execute_with_file(self):
        tt = TagSectionInfoTemplate(
            tag='tag_${NOX}_x',
            file='./r${NOD}.md'
        )

        with FilePool({'tag_233_x': 'README.md'}) as pool:
            t = tt(pool=pool, environ=dict(NOX='233', NOD='eadme'))
            with pytest.warns(RuntimeWarning):
                with open('README.md', 'r') as of:
                    assert t() == (True, of.read())

    def test_call_execute_from_dir(self):
        tt = TagSectionInfoTemplate(
            tag='tag_${NOX}_x',
            file='./R${NOD}.md'
        )

        with FilePool({'tag_233_x': os.curdir}) as pool:
            t = tt(pool=pool, environ=dict(NOX='233', NOD='EADME'))

            with open('README.md', 'r') as of:
                assert t() == (True, of.read())

    def test_call_execute_from_dir_without_file(self):
        tt = TagSectionInfoTemplate(
            tag='tag_${NOX}_x',
        )

        with FilePool({'tag_233_x': os.curdir}) as pool:
            t = tt(pool=pool, environ=dict(NOX='233', NOD='EADME'))
            assert t() == (False, None)


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
