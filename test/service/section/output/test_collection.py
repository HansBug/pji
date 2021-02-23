import os
import shutil
import tempfile

import pytest

from pji.service.section.output import FileOutputCollectionTemplate, CopyFileOutputTemplate, TagFileOutputTemplate, \
    CopyFileOutput, TagFileOutput
from pji.utils import FilePool


@pytest.mark.unittest
class TestServiceSectionOutputCollection:
    def test_simple(self):
        fct = FileOutputCollectionTemplate(
            CopyFileOutputTemplate(local='./${DIR}/r.md', file='r${V}.md'),
            TagFileOutputTemplate(local='./${DIR}/r.md', tag='tag_${V}_x'),
        )

        assert len(fct.outputs) == 2
        assert isinstance(fct.outputs[0], CopyFileOutputTemplate)
        assert isinstance(fct.outputs[1], TagFileOutputTemplate)
        assert repr(fct) == "<FileOutputCollectionTemplate outputs: 2>"

    def test_template_call(self):
        fct = FileOutputCollectionTemplate(
            CopyFileOutputTemplate(local='./${DIR}/r.md', file='r${V}.md'),
            TagFileOutputTemplate(local='./${DIR}/r.md', tag='tag_${V}_x'),
        )

        with tempfile.TemporaryDirectory() as wtd, \
                tempfile.TemporaryDirectory() as ttd, \
                FilePool()as pool:
            fc = fct(scriptdir=ttd, workdir=wtd, pool=pool, environ=dict(V='233', DIR='123'))

            assert len(fc.outputs)
            assert isinstance(fc.outputs[0], CopyFileOutput)
            assert isinstance(fc.outputs[1], TagFileOutput)
            assert repr(fc) == "<FileOutputCollection outputs: 2>"

    def test_template_execute(self):
        fct = FileOutputCollectionTemplate(
            CopyFileOutputTemplate(local='./${DIR}/r.md', file='${DIR}/r${V}.md'),
            TagFileOutputTemplate(local='./${DIR}/r.md', tag='tag_${V}_x'),
        )

        with tempfile.TemporaryDirectory() as wtd, \
                tempfile.TemporaryDirectory() as ttd, \
                FilePool()as pool:
            os.makedirs(os.path.join(wtd, '123'), exist_ok=True)
            shutil.copyfile('README.md', os.path.join(wtd, '123', 'r.md'))

            fc = fct(scriptdir=ttd, workdir=wtd, pool=pool, environ=dict(V='233', DIR='123'))
            fc()

            _copy_target_file = os.path.join(ttd, '123', 'r233.md')
            assert os.path.exists(_copy_target_file)
            assert os.path.isfile(_copy_target_file)
            with open('README.md', 'rb') as of, \
                    open(_copy_target_file, 'rb') as tf:
                assert of.read() == tf.read()

            _tag_target_file = pool['tag_233_x']
            assert os.path.exists(_tag_target_file)
            assert os.path.isfile(_tag_target_file)
            with open('README.md', 'rb') as of, \
                    open(_tag_target_file, 'rb') as tf:
                assert of.read() == tf.read()

    def test_loads(self):
        fct = FileOutputCollectionTemplate(
            CopyFileOutputTemplate(local='./${DIR}/r.md', file='${DIR}/r${V}.md'),
            TagFileOutputTemplate(local='./${DIR}/r.md', tag='tag_${V}_x'),
        )
        assert FileOutputCollectionTemplate.loads(fct) == fct

        assert len(FileOutputCollectionTemplate.loads(
            CopyFileOutputTemplate(local='./${DIR}/r.md', file='${DIR}/r${V}.md'),
        ).outputs) == 1
        assert len(FileOutputCollectionTemplate.loads([
            CopyFileOutputTemplate(local='./${DIR}/r.md', file='${DIR}/r${V}.md'),
            TagFileOutputTemplate(local='./${DIR}/r.md', tag='tag_${V}_x'),
        ]).outputs) == 2
        assert len(FileOutputCollectionTemplate.loads(
            dict(type='copy', local='./${DIR}/r.md', file='${DIR}/r${V}.md'),
        ).outputs) == 1
        with pytest.raises(TypeError):
            FileOutputCollectionTemplate.loads(123)


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
