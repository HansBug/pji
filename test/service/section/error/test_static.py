import os

import pytest

from pji.service.section.error import StaticErrorInfoTemplate


@pytest.mark.unittest
class TestServiceSectionErrorStatic:
    def test_simple(self):
        st = StaticErrorInfoTemplate(value='sdfglsdfkj${NO}')

        assert st.value == 'sdfglsdfkj${NO}'
        assert repr(st) == "<StaticErrorInfoTemplate value: 'sdfglsdfkj${NO}'>"

    def test_call(self):
        st = StaticErrorInfoTemplate(value='sdfglsdfkj${NO}')

        t = st(environ=dict(NO='233'))
        assert t.value == 'sdfglsdfkj233'
        assert repr(t) == "<StaticErrorInfo value: 'sdfglsdfkj233'>"

    def test_call_with_non_string(self):
        st = StaticErrorInfoTemplate(value=2147483647)

        t = st(environ=dict(NO='233'))
        assert t.value == 2147483647
        assert repr(t) == "<StaticErrorInfo value: 2147483647>"

    def test_call_execute(self):
        st = StaticErrorInfoTemplate(value='sdfglsdfkj${NO}')

        t = st(environ=dict(NO='233'))
        assert t() == 'sdfglsdfkj233'

    def test_call_execute_with_non_string(self):
        st = StaticErrorInfoTemplate(value=2147483647)

        t = st(environ=dict(NO='233'))
        assert t() == 2147483647


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
