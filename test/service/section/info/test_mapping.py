import codecs
import os
import shutil
import tempfile

import pytest

from pji.service.section.info import SectionInfoMappingTemplate, StaticSectionInfoTemplate, LocalSectionInfoTemplate, \
    TagSectionInfoTemplate, StaticSectionInfo, LocalSectionInfo, TagSectionInfo
from pji.utils import FilePool


@pytest.mark.unittest
class TestServiceSectionInfoMapping:
    def test_template(self):
        smt = SectionInfoMappingTemplate(
            static=StaticSectionInfoTemplate(value='233${V}'),
            local=LocalSectionInfoTemplate(file='./r${V}.md'),
            tag=TagSectionInfoTemplate(tag='tag_${V}'),
        )

        assert len(smt.items.keys()) == 3
        assert repr(smt) == "<SectionInfoMappingTemplate keys: ('local', 'static', 'tag')>"

        dict_data = dict(smt.__iter__())
        assert len(dict_data) == 3
        assert isinstance(dict_data['static'], StaticSectionInfoTemplate)
        assert isinstance(dict_data['local'], LocalSectionInfoTemplate)
        assert isinstance(dict_data['tag'], TagSectionInfoTemplate)

    def test_template_call(self):
        smt = SectionInfoMappingTemplate(
            static=StaticSectionInfoTemplate(value='233${V}'),
            local=LocalSectionInfoTemplate(file='./r${V}.md'),
            tag=TagSectionInfoTemplate(tag='tag_${V}'),
        )

        with tempfile.TemporaryDirectory() as wtd, \
                FilePool({'tag_233': 'README.md'}) as pool:
            sm = smt(pool=pool, workdir=wtd, environ=dict(V='233'))

            assert len(sm.items.keys()) == 3
            assert repr(sm) == "<SectionInfoMapping keys: ('local', 'static', 'tag')>"

            dict_data = dict(sm.__iter__())
            assert len(dict_data) == 3
            assert isinstance(dict_data['static'], StaticSectionInfo)
            assert isinstance(dict_data['local'], LocalSectionInfo)
            assert isinstance(dict_data['tag'], TagSectionInfo)

    def test_template_execute(self):
        smt = SectionInfoMappingTemplate(
            static=StaticSectionInfoTemplate(value='233${V}'),
            local=LocalSectionInfoTemplate(file='./r${V}.md'),
            tag=TagSectionInfoTemplate(tag='tag_${V}'),
        )

        with tempfile.TemporaryDirectory() as wtd, \
                FilePool({'tag_233': 'README.md'}) as pool:
            shutil.copyfile('README.md', os.path.join(wtd, 'r233.md'))

            sm = smt(pool=pool, workdir=wtd, environ=dict(V='233'))
            _result = sm()

            with codecs.open('README.md', 'r') as rf:
                _readme = rf.read()
            assert _result == {
                'static': '233233',
                'local': _readme,
                'tag': _readme,
            }

    def test_loads(self):
        smt = SectionInfoMappingTemplate(
            static=StaticSectionInfoTemplate(value='233${V}'),
            local=LocalSectionInfoTemplate(file='./r${V}.md'),
            tag=TagSectionInfoTemplate(tag='tag_${V}'),
        )
        assert SectionInfoMappingTemplate.loads(smt) == smt

        assert sorted(SectionInfoMappingTemplate.loads(dict(
            static=StaticSectionInfoTemplate(value='233${V}'),
            local=LocalSectionInfoTemplate(file='./r${V}.md'),
            tag=TagSectionInfoTemplate(tag='tag_${V}'),
        )).items.keys()) == sorted(['static', 'local', 'tag'])

        with pytest.raises(TypeError):
            SectionInfoMappingTemplate.loads([])


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
