import os
import tempfile
import warnings

import pytest
from pysystem import chmod, SystemUser

from pji.utils.file import FilePool


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestUtilsFile:
    def test_simple(self):
        with FilePool() as pool:
            assert isinstance(pool, FilePool)
            pool['readme'] = 'README.md'
            assert 'readme' in pool

            _root_dir = os.path.normpath(os.path.join(pool['readme'], '..', '..'))
            assert os.path.exists(_root_dir)
            assert os.path.isdir(_root_dir)

            with open('README.md', 'rb') as of, \
                    open(pool['readme'], 'rb') as tf:
                assert of.read() == tf.read()

            del pool['readme']
            assert 'readme' not in pool
            with pytest.raises(KeyError):
                _ = pool['readme']

        assert not os.path.exists(_root_dir)

    def test_with_init(self):
        with FilePool({'readme': 'README.md'}) as pool:
            assert isinstance(pool, FilePool)
            assert 'readme' in pool

            _root_dir = os.path.normpath(os.path.join(pool['readme'], '..', '..'))
            assert os.path.exists(_root_dir)
            assert os.path.isdir(_root_dir)

            with open('README.md', 'rb') as of, \
                    open(pool['readme'], 'rb') as tf:
                assert of.read() == tf.read()

            del pool['readme']
            assert 'readme' not in pool
            with pytest.raises(KeyError):
                _ = pool['readme']

        assert not os.path.exists(_root_dir)

    def test_dir(self):
        with FilePool({'source': 'pji', 'test': 'test'}) as pool:
            assert isinstance(pool, FilePool)
            assert 'source' in pool
            assert 'test' in pool

            _root_dir = os.path.normpath(os.path.join(pool['source'], '..', '..'))
            with open(os.path.join(pool['source'], '__init__.py'), 'rb') as pf, \
                    open(os.path.join('pji', '__init__.py'), 'rb') as of:
                assert pf.read() == of.read()
            with open(os.path.join(pool['source'], 'config', 'meta.py'), 'rb') as pf, \
                    open(os.path.join('pji', 'config', 'meta.py'), 'rb') as of:
                assert pf.read() == of.read()
            with open(os.path.join(pool['test'], '__init__.py'), 'rb') as pf, \
                    open(os.path.join('test', '__init__.py'), 'rb') as of:
                assert pf.read() == of.read()

            del pool['test']
            assert 'test' not in pool
            assert 'source' in pool
            with pytest.raises(KeyError):
                _ = pool['test']

        assert not os.path.exists(_root_dir)

    def test_file_not_found(self):
        with FilePool() as pool:
            assert isinstance(pool, FilePool)
            with pytest.raises(FileNotFoundError):
                pool['file_not_found'] = '/file/not/found'

    def test_file_access_denied(self):
        if SystemUser.current().name != 'root':
            with FilePool() as pool, \
                    tempfile.NamedTemporaryFile() as tf:
                assert isinstance(pool, FilePool)

                chmod(tf.name, '000')
                with pytest.raises(PermissionError):
                    pool['access_denied'] = tf.name
        else:
            warnings.warn(UserWarning('Non-root user expected but {actual} found, this test is skipped.'.format(
                actual=repr(SystemUser.current().name))))

    def test_init_failed(self):
        with pytest.raises(FileNotFoundError):
            with FilePool({'readme': '/file/not/found'}):
                pytest.fail('Should not reach here.')

    def test_invalid_tag(self):
        with pytest.raises(KeyError):
            with FilePool({'read  me': 'README.md'}):
                pytest.fail('Should not reach here.')

    def test_replace(self):
        with FilePool({'readme': 'README.md'}) as pool:
            assert isinstance(pool, FilePool)
            assert 'readme' in pool

            _root_dir = os.path.normpath(os.path.join(pool['readme'], '..', '..'))
            assert os.path.exists(_root_dir)
            assert os.path.isdir(_root_dir)

            with open('README.md', 'rb') as of, \
                    open(pool['readme'], 'rb') as tf:
                assert of.read() == tf.read()

            pool['readme'] = 'test/__init__.py'
            with open('test/__init__.py', 'rb') as of, \
                    open(pool['readme'], 'rb') as tf:
                assert of.read() == tf.read()

        assert not os.path.exists(_root_dir)

    def test_export_file(self):
        with FilePool({'readme': 'README.md'}) as pool:
            assert isinstance(pool, FilePool)
            assert 'readme' in pool

            _root_dir = os.path.normpath(os.path.join(pool['readme'], '..', '..'))
            with tempfile.NamedTemporaryFile() as f:
                pool.export('readme', f.name)
                with open(f.name, 'rb') as ef, \
                        open('README.md', 'rb') as of:
                    assert ef.read() == of.read()

        assert not os.path.exists(_root_dir)

    def test_export_dir(self):
        with FilePool({'source': 'pji', 'test': 'test'}) as pool:
            assert isinstance(pool, FilePool)
            assert 'source' in pool
            assert 'test' in pool

            _root_dir = os.path.normpath(os.path.join(pool['source'], '..', '..'))
            with tempfile.TemporaryDirectory() as td:
                pool.export('source', td)
                with open(os.path.join('pji', '__init__.py'), 'rb') as of, \
                        open(os.path.join(td, '__init__.py'), 'rb') as ef:
                    assert of.read() == ef.read()

    def test_clear(self):
        with FilePool({'source': 'pji', 'test': 'test'}) as pool:
            assert isinstance(pool, FilePool)
            assert 'source' in pool
            assert 'test' in pool

            _root_dir = os.path.normpath(os.path.join(pool['source'], '..', '..'))
            _source_dir = os.path.normpath(os.path.join(pool['source'], '..'))
            _test_dir = os.path.normpath(os.path.join(pool['test'], '..'))
            assert os.path.exists(_source_dir)
            assert os.path.exists(_test_dir)

            pool.clear()
            assert 'source' not in pool
            assert 'test' not in pool
            assert not os.path.exists(_source_dir)
            assert not os.path.exists(_test_dir)

    def test_close(self):
        pool = FilePool()
        try:
            assert isinstance(pool, FilePool)
            pool['readme'] = 'README.md'
            assert 'readme' in pool

            _root_dir = os.path.normpath(os.path.join(pool['readme'], '..', '..'))
            assert os.path.exists(_root_dir)
            assert os.path.isdir(_root_dir)

            with open('README.md', 'rb') as of, \
                    open(pool['readme'], 'rb') as tf:
                assert of.read() == tf.read()

            del pool['readme']
            assert 'readme' not in pool
            with pytest.raises(KeyError):
                _ = pool['readme']
        finally:
            pool.close()

        assert not os.path.exists(_root_dir)


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
