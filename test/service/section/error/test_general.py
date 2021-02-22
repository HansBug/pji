import os

import pytest

from pji.service.section.error import ErrorInfoType, load_error_template, LocalErrorInfoTemplate, TagErrorInfoTemplate, \
    StaticErrorInfoTemplate


@pytest.mark.unittest
class TestServiceSectionErrorGeneral:
    def test_type(self):
        assert ErrorInfoType.loads(ErrorInfoType.LOCAL) == ErrorInfoType.LOCAL
        assert ErrorInfoType.loads(ErrorInfoType.TAG) == ErrorInfoType.TAG
        assert ErrorInfoType.loads(ErrorInfoType.STATIC) == ErrorInfoType.STATIC
        assert ErrorInfoType.loads('local') == ErrorInfoType.LOCAL
        assert ErrorInfoType.loads('TAG') == ErrorInfoType.TAG
        assert ErrorInfoType.loads('Static') == ErrorInfoType.STATIC
        assert ErrorInfoType.loads(1) == ErrorInfoType.LOCAL
        assert ErrorInfoType.loads(2) == ErrorInfoType.TAG
        assert ErrorInfoType.loads(3) == ErrorInfoType.STATIC

    def test_type_invalid(self):
        with pytest.raises(KeyError):
            ErrorInfoType.loads('kdjfg')
        with pytest.raises(ValueError):
            ErrorInfoType.loads(-1)
        with pytest.raises(TypeError):
            ErrorInfoType.loads([])

    def test_load_template_local(self):
        et = load_error_template(dict(type='local', file='./1/2/3'))
        assert isinstance(et, LocalErrorInfoTemplate)
        assert et.file == './1/2/3'

    def test_load_template_tag(self):
        tt = load_error_template(dict(type='tag', tag='xxx', file='./1/2'))
        assert isinstance(tt, TagErrorInfoTemplate)
        assert tt.tag == 'xxx'
        assert tt.file == './1/2'

    def test_load_template_static(self):
        st = load_error_template(dict(type='static', value='89032'))
        assert isinstance(st, StaticErrorInfoTemplate)
        assert st.value == '89032'

    def test_load_template_self(self):
        et = load_error_template(dict(type='local', file='./1/2/3'))
        assert load_error_template(et) is et

    def test_load_template_invalid(self):
        with pytest.raises(KeyError):
            load_error_template(dict(type='xxx', file='xxx'))
        with pytest.raises(KeyError):
            load_error_template(dict(type_='local', file='./1/2/3'))
        with pytest.raises(TypeError):
            load_error_template(dict(type='local', tag='233'))
        with pytest.raises(TypeError):
            load_error_template([])


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
