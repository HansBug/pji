import os
import shutil
import tempfile

import pytest

from pji.service.section.output.tag import TagFileOutputTemplate
from pji.utils import FilePool


@pytest.mark.unittest
class TestServiceSectionOutputTag:
    def test_simple(self):
        tt = TagFileOutputTemplate(
            local='./r.md',
            tag='tag_x',
        )

        assert tt.local == './r.md'
        assert tt.tag == 'tag_x'

    def test_simple_repr(self):
        tt = TagFileOutputTemplate(
            local='./r.md',
            tag='tag_x',
        )

        assert repr(tt) == "<TagFileOutputTemplate local: './r.md', tag: 'tag_x'>"

    def test_call(self):
        tt = TagFileOutputTemplate(
            local='./r.md',
            tag='tag_x_${NO}',
        )

        with tempfile.TemporaryDirectory() as wtd, \
                FilePool() as pool:
            shutil.copyfile('README.md', os.path.join(wtd, 'r.md'))

            t = tt(workdir=wtd, pool=pool, environ=dict(NO="233"))
            assert t.local == os.path.abspath(os.path.join(wtd, 'r.md'))
            assert t.tag == 'tag_x_233'

    def test_call_execute(self):
        tt = TagFileOutputTemplate(
            local='./${NO}/r.md',
            tag='tag_x_${NO}',
        )

        with tempfile.TemporaryDirectory() as wtd, \
                FilePool() as pool:
            os.makedirs(os.path.join(wtd, '233'), exist_ok=True)
            shutil.copyfile('README.md', os.path.join(wtd, '233', 'r.md'))

            t = tt(workdir=wtd, pool=pool, environ=dict(NO="233"))
            t()
            assert 'tag_x_233' in pool

            _target_file = pool['tag_x_233']
            assert os.path.exists(_target_file)
            assert os.path.isfile(_target_file)

            with open('README.md', 'rb') as of, \
                    open(_target_file, 'rb') as tf:
                assert of.read() == tf.read()

    def test_call_execute_with_dir(self):
        tt = TagFileOutputTemplate(
            local='./${NO}/test',
            tag='tag_x_${NO}',
        )

        with tempfile.TemporaryDirectory() as wtd, \
                FilePool() as pool:
            os.makedirs(os.path.join(wtd, '233'), exist_ok=True)
            shutil.copytree('test', os.path.join(wtd, '233', 'test'))

            t = tt(workdir=wtd, pool=pool, environ=dict(NO="233"))
            t()
            assert 'tag_x_233' in pool

            _target_dir = pool['tag_x_233']
            assert os.path.exists(_target_dir)
            assert os.path.isdir(_target_dir)

            with open(os.path.join('test', '__init__.py'), 'rb') as of, \
                    open(os.path.join(_target_dir, '__init__.py'), 'rb') as tf:
                assert of.read() == tf.read()


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
