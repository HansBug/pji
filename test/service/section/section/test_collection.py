import codecs
import os
import tempfile

import pytest

from pji.service.section.section.collection import SectionCollectionTemplate, SectionCollection
from pji.utils import FilePool
from .base import _SECTION_1_TEMPLATE, _SECTION_2_TEMPLATE, _COMPLEX_TEXT


@pytest.mark.unittest
class TestServiceSectionSectionCollection:
    def test_template_simple(self):
        sct = SectionCollectionTemplate(_SECTION_1_TEMPLATE, _SECTION_2_TEMPLATE)

        assert len(sct.sections) == 2
        assert sct.sections[0].name == 'name_${V}'
        assert sct.sections[1].name == 'name_2_${V}'
        assert list(sct)[0].name == 'name_${V}'
        assert list(sct)[1].name == 'name_2_${V}'
        assert repr(sct) == "<SectionCollectionTemplate sections: 2>"

    def test_template_call(self):
        sct = SectionCollectionTemplate(_SECTION_1_TEMPLATE, _SECTION_2_TEMPLATE)

        with tempfile.TemporaryDirectory() as scriptdir:
            with codecs.open(os.path.join(scriptdir, 'README.md'), 'w') as of:
                of.write(_COMPLEX_TEXT)
            sc = sct(
                scriptdir=scriptdir,
                identification='nobody',
                resources=dict(max_real_time='1.8s'),
                environ=dict(ENV='xxx', VF='123'),
            )

            assert isinstance(sc, SectionCollection)
            assert len(sc.section_getters) == 2
            assert len(list(sc)) == 2
            assert repr(sc) == '<SectionCollection sections: 2>'

    def test_template_call_invalid(self):
        sct = SectionCollectionTemplate(_SECTION_1_TEMPLATE, _SECTION_2_TEMPLATE)

        with tempfile.TemporaryDirectory() as scriptdir:
            with codecs.open(os.path.join(scriptdir, 'README.md'), 'w') as of:
                of.write(_COMPLEX_TEXT)

            with pytest.raises(KeyError):
                with FilePool() as pool:
                    sct(
                        pool=pool,
                        scriptdir=scriptdir,
                        identification='nobody',
                        resources=dict(max_real_time='1.8s'),
                        environ=dict(ENV='xxx', VF='123'),
                    )
            with pytest.raises(KeyError):
                sct(
                    scriptdir=scriptdir,
                    identification='nobody',
                    resources=dict(max_real_time='1.8s'),
                    environ=dict(ENV='xxx', V='123'),
                )


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
