import os
import shutil
import tempfile

import pytest

from pji.control.model import Identification, ResourceLimit
from pji.utils import FilePool
from .base import _SECTION_TEMPLATE


@pytest.mark.unittest
class TestServiceSectionSectionSection:
    __DEMO_TEMPLATE = _SECTION_TEMPLATE

    def test_section_simple(self):
        with tempfile.TemporaryDirectory() as scriptdir, \
                FilePool() as pool:
            shutil.copyfile('README.md', os.path.join(scriptdir, 'README.md'))
            s = self.__DEMO_TEMPLATE(
                scriptdir=scriptdir,
                pool=pool,
                identification='nobody',
                resources=dict(max_real_time='2.0s'),
                environ=dict(ENV='xxx'),
            )

            assert s.name == 'name_233'
            assert s.identification == Identification.loads('nobody')
            assert s.resources == ResourceLimit.loads({'max_real_time': '2.0s'})
            assert s.environ == {'V': '233', 'ENV': 'xxx'}

    def test_section_invalid(self):
        with tempfile.TemporaryDirectory() as scriptdir, \
                FilePool() as pool:
            shutil.copyfile('README.md', os.path.join(scriptdir, 'README.md'))
            with pytest.raises(KeyError):
                self.__DEMO_TEMPLATE(
                    workdir=os.curdir,
                    scriptdir=scriptdir,
                    pool=pool,
                    identification='nobody',
                    resources=dict(max_real_time='2.0s'),
                    environ=dict(ENV='xxx'),
                )

    def test_section_call(self):
        with tempfile.TemporaryDirectory() as scriptdir, \
                FilePool() as pool:
            shutil.copyfile('README.md', os.path.join(scriptdir, 'README.md'))
            s = self.__DEMO_TEMPLATE(
                scriptdir=scriptdir,
                pool=pool,
                identification='nobody',
                resources=dict(max_real_time='2.0s'),
                environ=dict(ENV='xxx'),
            )
            _success, _results, _infos = s()

            assert _success
            assert len(_results) == 4
            assert _results[0].ok
            assert _results[1].ok
            assert _results[2].ok
            assert _results[3].ok
            assert _infos == {'static': 'this is v : 233', 'value': 233,
                              'local': '# pji\n\nAn easy-to-use python interaction for judgement.',
                              'tag': '# pji\n\nAn easy-to-use python interaction for judgement.',
                              'base64': 'IyBwamkKCkFuIGVhc3ktdG8tdXNlIHB5dGhvbiBpbn'
                                        'RlcmFjdGlvbiBmb3IganVkZ2VtZW50Lg==\n'}


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
