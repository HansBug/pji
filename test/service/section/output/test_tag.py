import os

import pytest
from hbutils.testing import isolated_directory

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

        assert repr(tt) == "<TagFileOutputTemplate local: './r.md', tag: 'tag_x', condition: required, on: success>"

    def test_call(self):
        tt = TagFileOutputTemplate(
            local='./r.md',
            tag='tag_x_${NO}',
        )

        with isolated_directory({'r.md': 'README.md'}), FilePool() as pool:
            t = tt(workdir='.', pool=pool, environ=dict(NO="233"))
            assert t.local == os.path.abspath('r.md')
            assert t.tag == 'tag_x_233'

    def test_call_execute(self):
        tt = TagFileOutputTemplate(
            local='./${NO}/r.md',
            tag='tag_x_${NO}',
        )
        original_path = os.path.abspath('.')

        with isolated_directory({'233/r.md': 'README.md'}), FilePool() as pool:
            t = tt(workdir='.', pool=pool, environ=dict(NO="233"))
            t(run_success=True)
            assert 'tag_x_233' in pool

            _target_file = pool['tag_x_233']
            assert os.path.exists(_target_file)
            assert os.path.isfile(_target_file)

            with open(os.path.join(original_path, 'README.md'), 'rb') as of, open(_target_file, 'rb') as tf:
                assert of.read() == tf.read()

    def test_call_execute_with_dir(self):
        tt = TagFileOutputTemplate(
            local='./${NO}/test',
            tag='tag_x_${NO}',
        )
        original_path = os.path.abspath('.')

        with isolated_directory({'233/test': 'test'}), FilePool() as pool:
            t = tt(workdir='.', pool=pool, environ=dict(NO="233"))
            t(run_success=True)
            assert 'tag_x_233' in pool

            _target_dir = pool['tag_x_233']
            assert os.path.exists(_target_dir)
            assert os.path.isdir(_target_dir)

            with open(os.path.join(original_path, 'test/utils/test_args.py'), 'rb') as of, \
                    open(os.path.join(_target_dir, 'utils/test_args.py'), 'rb') as tf:
                assert of.read() == tf.read()
