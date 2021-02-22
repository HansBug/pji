import os

import pytest
from pysystem import FileAuthority

from pji.service.section import FileInputType, autoload_template, CopyFileInputTemplate, LinkFileInputTemplate, \
    TagFileInputTemplate


@pytest.mark.unittest
class TestServiceSectionInputGeneral:
    def test_file_input_type(self):
        assert FileInputType.loads(FileInputType.COPY) == FileInputType.COPY
        assert FileInputType.loads(FileInputType.LINK) == FileInputType.LINK
        assert FileInputType.loads(FileInputType.TAG) == FileInputType.TAG
        assert FileInputType.loads('copy') == FileInputType.COPY
        assert FileInputType.loads('LINK') == FileInputType.LINK
        assert FileInputType.loads('Tag') == FileInputType.TAG
        assert FileInputType.loads(1) == FileInputType.COPY
        assert FileInputType.loads(2) == FileInputType.LINK
        assert FileInputType.loads(3) == FileInputType.TAG

    def test_file_input_type_invalid(self):
        with pytest.raises(KeyError):
            FileInputType.loads('kfsdlsd')
        with pytest.raises(ValueError):
            FileInputType.loads(-1)
        with pytest.raises(TypeError):
            FileInputType.loads([])

    def test_autoload_template_copy(self):
        ct = autoload_template(dict(type='copy', file='/this/is/file', local='./file', privilege='rw-'))
        assert isinstance(ct, CopyFileInputTemplate)
        assert ct.file == '/this/is/file'
        assert ct.local == './file'
        assert ct.privilege == FileAuthority.loads('rw-------')

    def test_autoload_template_link(self):
        lnt = autoload_template(dict(type='link', file='/this/is/file', local='./file'))
        assert isinstance(lnt, LinkFileInputTemplate)
        assert lnt.file == '/this/is/file'
        assert lnt.local == './file'

    def test_autoload_template_tag(self):
        tt = autoload_template(dict(type='tag', tag='djgfld', local='./file', privilege='777'))
        assert isinstance(tt, TagFileInputTemplate)
        assert tt.tag == 'djgfld'
        assert tt.local == './file'
        assert tt.privilege == FileAuthority.loads('rwxrwxrwx')

    def test_autoload_template_invalid(self):
        with pytest.raises(KeyError):
            autoload_template(dict(type='tag_', tag='djgfld', local='./file', privilege='777'))
        with pytest.raises(KeyError):
            autoload_template(dict(type_='tag', tag='djgfld', local='./file', privilege='777'))
        with pytest.raises(TypeError):
            autoload_template(dict(type='link', file='/this/is/file', local='./file', privilege='777'))


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
