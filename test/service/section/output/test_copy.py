import os
import shutil
import tempfile

import pytest

from pji.service.section.output import CopyFileOutputTemplate


@pytest.mark.unittest
class TestServiceSectionOutputCopy:
    def test_simple(self):
        ct = CopyFileOutputTemplate(
            local='./r.md',
            file='${DIR}/r.md',
        )

        assert ct.local == './r.md'
        assert ct.file == '${DIR}/r.md'

    def test_simple_repr(self):
        ct = CopyFileOutputTemplate(
            local='./r.md',
            file='${DIR}/r.md',
        )

        assert repr(ct) == "<CopyFileOutputTemplate local: './r.md', file: '${DIR}/r.md', condition: required, on: success>"

    def test_call(self):
        ct = CopyFileOutputTemplate(
            local='./r.md',
            file='${DIR}/r.md',
        )

        with tempfile.TemporaryDirectory() as wtd, \
                tempfile.TemporaryDirectory() as ttd:
            shutil.copyfile('README.md', os.path.join(wtd, 'r.md'))

            c = ct(scriptdir=os.curdir, workdir=wtd, environ=dict(DIR=ttd))
            assert c.local == os.path.abspath(os.path.join(wtd, 'r.md'))
            assert c.file == os.path.abspath(os.path.join(ttd, 'r.md'))

    def test_call_invalid(self):
        ct = CopyFileOutputTemplate(
            local='./${DIR}/r.md',
            file='${DIR}/r.md',
        )

        with tempfile.TemporaryDirectory() as wtd:
            with pytest.raises(ValueError):
                ct(scriptdir=os.curdir, workdir=wtd, environ=dict(DIR='..'))

    def test_call_execute(self):
        ct = CopyFileOutputTemplate(
            local='./r.md',
            file='${DIR}/r.md',
        )

        with tempfile.TemporaryDirectory() as wtd, \
                tempfile.TemporaryDirectory() as ttd:
            shutil.copyfile('README.md', os.path.join(wtd, 'r.md'))

            c = ct(scriptdir=os.curdir, workdir=wtd, environ=dict(DIR=ttd))
            c()

            _target_file = os.path.join(ttd, 'r.md')
            assert os.path.exists(_target_file)
            with open('README.md', 'rb') as of, \
                    open(_target_file, 'rb') as tf:
                assert of.read() == tf.read()

    def test_call_execute_with_dir(self):
        ct = CopyFileOutputTemplate(
            local='test',
            file='${DIR}/test',
        )

        with tempfile.TemporaryDirectory() as wtd, \
                tempfile.TemporaryDirectory() as ttd:
            shutil.copytree('test', os.path.join(wtd, 'test'))

            c = ct(scriptdir=ttd, workdir=wtd, environ=dict(DIR='1/2/3'))
            c()

            _target_dir = os.path.join(ttd, '1/2/3', 'test')
            assert os.path.exists(_target_dir)
            assert os.path.isdir(_target_dir)
            with open(os.path.join('test', '__init__.py'), 'rb') as of, \
                    open(os.path.join(ttd, '1/2/3', 'test', '__init__.py'), 'rb') as tf:
                assert of.read() == tf.read()
