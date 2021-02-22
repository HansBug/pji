import os

import pytest

from pji.service.section import FileOutputType, autoload_output_template, TagFileOutputTemplate, CopyFileOutputTemplate


@pytest.mark.unittest
class TestServiceSectionOutputGeneral:
    def test_file_output_type(self):
        assert FileOutputType.loads(FileOutputType.COPY) == FileOutputType.COPY
        assert FileOutputType.loads(FileOutputType.TAG) == FileOutputType.TAG
        assert FileOutputType.loads('copy') == FileOutputType.COPY
        assert FileOutputType.loads('Tag') == FileOutputType.TAG
        assert FileOutputType.loads(1) == FileOutputType.COPY
        assert FileOutputType.loads(2) == FileOutputType.TAG

    def test_file_output_type_invalid(self):
        with pytest.raises(KeyError):
            FileOutputType.loads('kfsdlsd')
        with pytest.raises(ValueError):
            FileOutputType.loads(-1)
        with pytest.raises(TypeError):
            FileOutputType.loads([])

    def test_autoload_template_copy(self):
        ct = autoload_output_template(dict(type='copy', file='/this/is/file', local='./file'))
        assert isinstance(ct, CopyFileOutputTemplate)
        assert ct.file == '/this/is/file'
        assert ct.local == './file'

    def test_autoload_template_tag(self):
        tt = autoload_output_template(dict(type='tag', tag='djgfld', local='./file'))
        assert isinstance(tt, TagFileOutputTemplate)
        assert tt.tag == 'djgfld'
        assert tt.local == './file'

    def test_autoload_template_invalid(self):
        with pytest.raises(KeyError):
            autoload_output_template(dict(type='tag_', tag='djgfld', local='./file'))
        with pytest.raises(KeyError):
            autoload_output_template(dict(type_='tag', tag='djgfld', local='./file'))
        with pytest.raises(TypeError):
            autoload_output_template(dict(type='tag', file='/this/is/file', local='./file'))


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
