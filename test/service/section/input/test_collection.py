import os
import tempfile

import pytest
from pysystem import FileAuthority, SystemUser, SystemGroup

from pji.service.section.input import FileInputCollectionTemplate, CopyFileInputTemplate, TagFileInputTemplate, \
    LinkFileInputTemplate, CopyFileInput, TagFileInput, LinkFileInput
from pji.utils import FilePool


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestServiceSectionInputCollection:
    def test_template(self):
        ict = FileInputCollectionTemplate(
            CopyFileInputTemplate(file='README.my', local='./${DIR}/rc.md', privilege='r--'),
            TagFileInputTemplate(tag='tag_${V}_r', local='./${DIR}/rt.md', privilege='rw-'),
            LinkFileInputTemplate(file='README.md', local='./${DIR}/rl.md'),
        )

        assert len(ict.items) == 3
        assert isinstance(ict.items[0], CopyFileInputTemplate)
        assert isinstance(ict.items[1], TagFileInputTemplate)
        assert isinstance(ict.items[2], LinkFileInputTemplate)
        assert repr(ict) == "<FileInputCollectionTemplate inputs: 3>"

        list_data = list(ict.__iter__())
        assert len(list_data) == 3
        assert isinstance(list_data[0], CopyFileInputTemplate)
        assert isinstance(list_data[1], TagFileInputTemplate)
        assert isinstance(list_data[2], LinkFileInputTemplate)

    def test_template_call(self):
        ict = FileInputCollectionTemplate(
            CopyFileInputTemplate(file='README.md', local='./${DIR}/rc.md', privilege='r--'),
            TagFileInputTemplate(tag='tag_${V}_r', local='./${DIR}/rt.md', privilege='rw-'),
            LinkFileInputTemplate(file='README.md', local='./${DIR}/rl.md'),
        )

        with tempfile.TemporaryDirectory() as wtd, \
                FilePool({'tag_233_r': 'README.md'}) as pool:
            ic = ict(scriptdir=os.curdir, workdir=wtd, pool=pool, identification='nobody',
                     environ=dict(DIR='123', V='233'))
            assert len(ic.items) == 3
            assert isinstance(ic.items[0], CopyFileInput)
            assert isinstance(ic.items[1], TagFileInput)
            assert isinstance(ic.items[2], LinkFileInput)
            assert repr(ic) == "<FileInputCollection inputs: 3>"

            list_data = list(ic.__iter__())
            assert len(list_data) == 3
            assert isinstance(list_data[0], CopyFileInput)
            assert isinstance(list_data[1], TagFileInput)
            assert isinstance(list_data[2], LinkFileInput)

    def test_template_execute(self):
        ict = FileInputCollectionTemplate(
            CopyFileInputTemplate(file='README.md', local='./${DIR}/rc.md', privilege='r--'),
            TagFileInputTemplate(tag='tag_${V}_r', local='./${DIR}/rt.md', privilege='rw-'),
            LinkFileInputTemplate(file='README.md', local='./${DIR}/rl.md'),
        )

        with tempfile.TemporaryDirectory() as wtd, \
                FilePool({'tag_233_r': 'README.md'}) as pool:
            ic = ict(scriptdir=os.curdir, workdir=wtd, pool=pool, identification='nobody',
                     environ=dict(DIR='123', V='233'))
            ic()

            _copy_target_file = os.path.join(wtd, '123', 'rc.md')
            assert os.path.exists(_copy_target_file)
            assert os.path.isfile(_copy_target_file)
            assert FileAuthority.load_from_file(_copy_target_file) == FileAuthority.loads('r--------')
            assert SystemUser.load_from_file(_copy_target_file) == SystemUser.loads('nobody')
            assert SystemGroup.load_from_file(_copy_target_file) == SystemGroup.loads('nogroup')
            with open('README.md', 'rb') as of, \
                    open(_copy_target_file, 'rb') as tf:
                assert of.read() == tf.read()

            _tag_target_file = os.path.join(wtd, '123', 'rt.md')
            assert os.path.exists(_tag_target_file)
            assert os.path.isfile(_tag_target_file)
            assert FileAuthority.load_from_file(_tag_target_file) == FileAuthority.loads('rw-------')
            assert SystemUser.load_from_file(_tag_target_file) == SystemUser.loads('nobody')
            assert SystemGroup.load_from_file(_tag_target_file) == SystemGroup.loads('nogroup')
            with open('README.md', 'rb') as of, \
                    open(_tag_target_file, 'rb') as tf:
                assert of.read() == tf.read()

            _link_target_file = os.path.join(wtd, '123', 'rl.md')
            assert os.path.exists(_link_target_file)
            assert os.path.isfile(_link_target_file)
            assert os.path.islink(_link_target_file)
            with open('README.md', 'rb') as of, \
                    open(_link_target_file, 'rb') as tf:
                assert of.read() == tf.read()

    def test_loads(self):
        ict = FileInputCollectionTemplate(
            CopyFileInputTemplate(file='README.md', local='./${DIR}/rc.md', privilege='r--'),
            TagFileInputTemplate(tag='tag_${V}_r', local='./${DIR}/rt.md', privilege='rw-'),
            LinkFileInputTemplate(file='README.md', local='./${DIR}/rl.md'),
        )
        assert FileInputCollectionTemplate.loads(ict) == ict

        assert len(FileInputCollectionTemplate.loads(
            LinkFileInputTemplate(file='README.md', local='./${DIR}/rl.md'),
        ).items) == 1
        assert len(FileInputCollectionTemplate.loads([
            CopyFileInputTemplate(file='README.md', local='./${DIR}/rc.md', privilege='r--'),
            TagFileInputTemplate(tag='tag_${V}_r', local='./${DIR}/rt.md', privilege='rw-'),
            LinkFileInputTemplate(file='README.md', local='./${DIR}/rl.md'),
        ]).items) == 3
        assert len(FileInputCollectionTemplate.loads([
            'copy:README.md:./${DIR}/rc.md:r--',
            'tag:tag_${V}_r:./${DIR}/rt.md:rw-',
            'link:README.md:./${DIR}/rl.md',
        ]).items) == 3
        assert len(FileInputCollectionTemplate.loads(
            dict(type='link', file='README.md', local='./${DIR}/rl.md')
        ).items) == 1
        with pytest.raises(TypeError):
            FileInputCollectionTemplate.loads(123)


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
