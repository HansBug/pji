import os
import tempfile

import pytest

from pji.service.section.input.link import LinkFileInputTemplate


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestServiceSectionInputLink:
    def test_template(self):
        lf = LinkFileInputTemplate(
            file='README.md',
            local='./r.md',
        )

        assert lf.file == 'README.md'
        assert lf.local == './r.md'

    def test_template_repr(self):
        lf = LinkFileInputTemplate(
            file='README.md',
            local='./r.md',
        )

        assert repr(lf) == "<LinkFileInputTemplate file: 'README.md', local: './r.md'>"

    def test_template_call_and_link(self):
        lf = LinkFileInputTemplate(
            file='README.md',
            local='./r.md',
        )
        with tempfile.TemporaryDirectory() as fd:
            ln = lf(os.curdir, fd)

            assert ln.file == os.path.abspath('README.md')
            assert ln.local == os.path.normpath(os.path.join(fd, 'r.md'))

    def test_template_call_invalid(self):
        lf = LinkFileInputTemplate(
            file='README.md',
            local='./${DIR}/r.md',
        )
        with tempfile.TemporaryDirectory() as fd:
            with pytest.raises(ValueError):
                lf(os.curdir, fd, dict(DIR='..'))
            with pytest.raises(KeyError):
                lf(os.curdir, fd, None)

    def test_link_repr(self):
        lf = LinkFileInputTemplate(
            file='README.md',
            local='./r.md',
        )
        with tempfile.TemporaryDirectory() as fd:
            ln = lf(os.curdir, fd)

            assert repr(ln) == "<LinkFileInput file: '{cur}/README.md', local: '{fd}/r.md'>".format(
                cur=os.path.abspath('.'), fd=fd)

    def test_link_call(self):
        lf = LinkFileInputTemplate(
            file='README.md',
            local='./r.md',
        )
        with tempfile.TemporaryDirectory() as fd:
            ln = lf(os.curdir, fd)
            ln()

            _target_file = os.path.normpath(os.path.join(fd, 'r.md'))
            assert os.path.exists(_target_file)
            assert os.path.islink(_target_file)
            with open('README.md', 'rb') as of, \
                    open(_target_file, 'rb') as tf:
                assert of.read() == tf.read()

    def test_link_call_dir(self):
        lf = LinkFileInputTemplate(
            file='pji',
            local='pinit.py',
        )
        with tempfile.TemporaryDirectory() as fd:
            ln = lf(os.curdir, fd)
            ln()

            _target_dir = os.path.normpath(os.path.join(fd, 'pinit.py'))
            assert os.path.exists(_target_dir)
            assert os.path.islink(_target_dir)
            with open(os.path.normpath(os.path.join('pji', '__init__.py')), 'rb') as of, \
                    open(os.path.normpath(os.path.join(_target_dir, '__init__.py')), 'rb') as tf:
                assert of.read() == tf.read()


if __name__ == '__main__':
    pass
