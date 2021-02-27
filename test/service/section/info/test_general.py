import os

import pytest

from pji.service.section.info import SectionInfoType, load_info_template, LocalSectionInfoTemplate, \
    TagSectionInfoTemplate, \
    StaticSectionInfoTemplate


@pytest.mark.unittest
class TestServiceSectionInfoGeneral:
    def test_type(self):
        assert SectionInfoType.loads(SectionInfoType.LOCAL) == SectionInfoType.LOCAL
        assert SectionInfoType.loads(SectionInfoType.TAG) == SectionInfoType.TAG
        assert SectionInfoType.loads(SectionInfoType.STATIC) == SectionInfoType.STATIC
        assert SectionInfoType.loads('local') == SectionInfoType.LOCAL
        assert SectionInfoType.loads('TAG') == SectionInfoType.TAG
        assert SectionInfoType.loads('Static') == SectionInfoType.STATIC
        assert SectionInfoType.loads(1) == SectionInfoType.LOCAL
        assert SectionInfoType.loads(2) == SectionInfoType.TAG
        assert SectionInfoType.loads(3) == SectionInfoType.STATIC

    def test_type_invalid(self):
        with pytest.raises(KeyError):
            SectionInfoType.loads('kdjfg')
        with pytest.raises(ValueError):
            SectionInfoType.loads(-1)
        with pytest.raises(TypeError):
            SectionInfoType.loads([])

    def test_load_template_local(self):
        et = load_info_template(dict(type='local', file='./1/2/3'))
        assert isinstance(et, LocalSectionInfoTemplate)
        assert et.file == './1/2/3'

        et = load_info_template('local:./1/2/3')
        assert isinstance(et, LocalSectionInfoTemplate)
        assert et.file == './1/2/3'

    def test_load_template_tag(self):
        tt = load_info_template(dict(type='tag', tag='xxx', file='./1/2'))
        assert isinstance(tt, TagSectionInfoTemplate)
        assert tt.tag == 'xxx'
        assert tt.file == './1/2'

        tt = load_info_template('tag:xxx:./1/2')
        assert isinstance(tt, TagSectionInfoTemplate)
        assert tt.tag == 'xxx'
        assert tt.file == './1/2'

    def test_load_template_static(self):
        st = load_info_template(dict(type='static', value='89032'))
        assert isinstance(st, StaticSectionInfoTemplate)
        assert st.value == '89032'

        st = load_info_template('static:89032')
        assert isinstance(st, StaticSectionInfoTemplate)
        assert st.value == '89032'

    def test_load_template_self(self):
        et = load_info_template(dict(type='local', file='./1/2/3'))
        assert load_info_template(et) is et

    def test_load_template_invalid(self):
        with pytest.raises(KeyError):
            load_info_template(dict(type='xxx', file='xxx'))
        with pytest.raises(KeyError):
            load_info_template(dict(type_='local', file='./1/2/3'))
        with pytest.raises(TypeError):
            load_info_template(dict(type='local', tag='233'))
        with pytest.raises(TypeError):
            load_info_template([])


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
