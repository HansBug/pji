import os

import pytest

from pji.service.section.info import StaticSectionInfoTemplate


@pytest.mark.unittest
class TestServiceSectionInfoStatic:
    def test_simple(self):
        st = StaticSectionInfoTemplate(value='sdfglsdfkj${NO}')

        assert st.value == 'sdfglsdfkj${NO}'
        assert repr(st) == "<StaticSectionInfoTemplate value: 'sdfglsdfkj${NO}'>"

    def test_call(self):
        st = StaticSectionInfoTemplate(value='sdfglsdfkj${NO}')

        t = st(environ=dict(NO='233'))
        assert t.value == 'sdfglsdfkj233'
        assert repr(t) == "<StaticSectionInfo value: 'sdfglsdfkj233'>"

    def test_call_with_non_string(self):
        st = StaticSectionInfoTemplate(value=2147483647)

        t = st(environ=dict(NO='233'))
        assert t.value == 2147483647
        assert repr(t) == "<StaticSectionInfo value: 2147483647>"

    def test_call_execute(self):
        st = StaticSectionInfoTemplate(value='sdfglsdfkj${NO}')

        t = st(environ=dict(NO='233'))
        assert t() == (True, 'sdfglsdfkj233')

    def test_call_execute_with_non_string(self):
        st = StaticSectionInfoTemplate(value=2147483647)

        t = st(environ=dict(NO='233'))
        assert t() == (True, 2147483647)


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
