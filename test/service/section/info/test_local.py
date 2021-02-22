import os
import shutil
import tempfile

import pytest

from pji.service.section.info.local import LocalSectionInfoTemplate


@pytest.mark.unittest
class TestServiceSectionInfoLocal:
    def test_simple(self):
        tl = LocalSectionInfoTemplate(file='./r.md')

        assert tl.file == './r.md'

    def test_simple_repr(self):
        tl = LocalSectionInfoTemplate(file='./r.md')

        assert repr(tl) == "<LocalSectionInfoTemplate file: './r.md'>"

    def test_call(self):
        tl = LocalSectionInfoTemplate(file='./${DIR}/r.md')

        with tempfile.TemporaryDirectory() as wtd:
            t = tl(workdir=wtd, environ=dict(DIR='1/2/3'))

            assert t.file == os.path.join(wtd, '1/2/3', 'r.md')

    def test_call_invalid(self):
        tl = LocalSectionInfoTemplate(file='./${DIR}/r.md')

        with tempfile.TemporaryDirectory() as wtd:
            with pytest.raises(ValueError):
                tl(workdir=wtd, environ=dict(DIR='../a/..'))

    def test_call_execute(self):
        tl = LocalSectionInfoTemplate(file='./${DIR}/r.md')
        with tempfile.TemporaryDirectory() as wtd:
            shutil.copyfile('README.md', os.path.join(wtd, 'r.md'))

            t = tl(workdir=wtd, environ=dict(DIR='.'))
            with open('README.md', 'r') as of:
                assert t() == of.read()

    def test_call_execute_invalid(self):
        tl = LocalSectionInfoTemplate(file='./${DIR}/r.md')
        with tempfile.TemporaryDirectory() as wtd:
            os.makedirs(os.path.join(wtd, '1/2/3/r.md/'), exist_ok=True)
            shutil.copyfile('README.md', os.path.join(wtd, '1/2/3/r.md/', 'r.md'))

            t = tl(workdir=wtd, environ=dict(DIR='1/2/3'))
            with pytest.raises(IsADirectoryError):
                t()


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
