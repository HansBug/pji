import os
import tempfile

import pytest
from hbutils.testing import isolated_directory

from pji.service.section.output import CopyFileOutputTemplate


# noinspection DuplicatedCode
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
        assert repr(CopyFileOutputTemplate(
            local='./r.md',
            file='${DIR}/r.md',
        )) == "<CopyFileOutputTemplate local: './r.md', file: '${DIR}/r.md', condition: required, on: success>"

    def test_call(self):
        ct = CopyFileOutputTemplate(
            local='./r.md',
            file='${DIR}/r.md',
        )
        original_path = os.path.abspath('.')

        with isolated_directory({'r.md': 'README.md'}), tempfile.TemporaryDirectory() as ttd:
            c = ct(scriptdir=original_path, workdir='.', environ=dict(DIR=ttd))
            assert c.local == os.path.abspath('r.md')
            assert c.file == os.path.abspath(os.path.join(ttd, 'r.md'))

    def test_call_invalid(self):
        ct = CopyFileOutputTemplate(
            local='./${DIR}/r.md',
            file='${DIR}/r.md',
        )
        original_path = os.path.abspath('.')

        with isolated_directory():
            with pytest.raises(ValueError):
                ct(scriptdir=original_path, workdir='.', environ=dict(DIR='..'))

    def test_call_execute(self):
        ct = CopyFileOutputTemplate(
            local='./r.md',
            file='${DIR}/r.md',
        )
        original_path = os.path.abspath('.')

        with isolated_directory({'r.md': 'README.md'}), tempfile.TemporaryDirectory() as ttd:
            c = ct(scriptdir=original_path, workdir='.', environ=dict(DIR=ttd))
            _is_complete = False

            def _complete():
                nonlocal _is_complete
                _is_complete = True

            c(run_success=True, output_complete=_complete)
            assert _is_complete

            assert os.path.exists('r.md')
            with open(os.path.join(original_path, 'README.md'), 'rb') as of, open('r.md', 'rb') as tf:
                assert of.read() == tf.read()

    def test_call_execute_with_dir(self):
        ct = CopyFileOutputTemplate(
            local='test',
            file='${DIR}/test',
        )
        original_path = os.path.abspath('.')

        with isolated_directory({'test': 'test'}), tempfile.TemporaryDirectory() as ttd:
            c = ct(scriptdir=ttd, workdir='.', environ=dict(DIR='1/2/3'))
            _is_complete = False

            def _complete():
                nonlocal _is_complete
                _is_complete = True

            c(run_success=True, output_complete=_complete)
            assert _is_complete

            _target_dir = os.path.join(ttd, '1/2/3', 'test')
            assert os.path.exists(_target_dir)
            assert os.path.isdir(_target_dir)
            with open(os.path.join(original_path, 'test', '__init__.py'), 'rb') as of, \
                    open(os.path.join(ttd, '1/2/3', 'test', '__init__.py'), 'rb') as tf:
                assert of.read() == tf.read()

    def test_call_failed(self):
        ct = CopyFileOutputTemplate(
            local='./rxxxxxxxxxxxxxx.md',
            file='${DIR}/r.md',
        )
        original_path = os.path.abspath('.')

        with isolated_directory({'r.md': 'README.md'}), tempfile.TemporaryDirectory() as ttd:
            c = ct(scriptdir=original_path, workdir='.', environ=dict(DIR=ttd))
            _is_start, _is_complete = False, False

            def _start():
                nonlocal _is_start
                _is_start = True

            def _complete():
                nonlocal _is_complete
                _is_complete = True

            with pytest.raises(FileNotFoundError):
                c(run_success=True, output_complete=_complete, output_start=_start)
            assert _is_start
            assert not _is_complete
            assert not os.path.exists(os.path.join(ttd, 'r.md'))

    def test_call_skipped(self):
        ct = CopyFileOutputTemplate(
            local='./rxxxxxxxxxxxxxx.md',
            file='${DIR}/r.md',
            condition='optional',
        )
        original_path = os.path.abspath('.')

        with isolated_directory({'r.md': 'README.md'}), tempfile.TemporaryDirectory() as ttd:
            c = ct(scriptdir=original_path, workdir='.', environ=dict(DIR=ttd))
            _is_start, _is_complete, _is_skipped = False, False, False

            def _start():
                nonlocal _is_start
                _is_start = True

            def _complete():
                nonlocal _is_complete
                _is_complete = True

            def _skip():
                nonlocal _is_skipped
                _is_skipped = True

            c(run_success=True, output_start=_start, output_complete=_complete, output_skip=_skip)
            assert _is_start
            assert not _is_complete
            assert _is_skipped
            assert not os.path.exists(os.path.join(ttd, 'r.md'))

    def test_call_on_success(self):
        ct = CopyFileOutputTemplate(
            local='./r.md',
            file='${DIR}/r.md',
            on_='success',
        )
        original_path = os.path.abspath('.')

        with isolated_directory({'r.md': 'README.md'}), tempfile.TemporaryDirectory() as ttd:
            c = ct(scriptdir=original_path, workdir='.', environ=dict(DIR=ttd))
            _is_start, _is_complete = False, False

            def _start():
                nonlocal _is_start
                _is_start = True

            def _complete():
                nonlocal _is_complete
                _is_complete = True

            c(run_success=True, output_start=_start, output_complete=_complete)
            assert _is_start
            assert _is_complete

            assert os.path.exists(os.path.join(ttd, 'r.md'))
            with open(os.path.join(original_path, 'README.md'), 'rb') as of, \
                    open(os.path.join(ttd, 'r.md'), 'rb') as tf:
                assert of.read() == tf.read()

        with isolated_directory({'r.md': 'README.md'}), tempfile.TemporaryDirectory() as ttd:
            c = ct(scriptdir=original_path, workdir='.', environ=dict(DIR=ttd))
            _is_start, _is_complete = False, False

            def _start():
                nonlocal _is_start
                _is_start = True

            def _complete():
                nonlocal _is_complete
                _is_complete = True

            c(run_success=False, output_start=_start, output_complete=_complete)
            assert not _is_start
            assert not _is_complete
            assert not os.path.exists(os.path.join(ttd, 'r.md'))

    def test_call_on_fail(self):
        ct = CopyFileOutputTemplate(
            local='./r.md',
            file='${DIR}/r.md',
            on_='fail',
        )
        original_path = os.path.abspath('.')

        with isolated_directory({'r.md': 'README.md'}), tempfile.TemporaryDirectory() as ttd:
            c = ct(scriptdir=original_path, workdir='.', environ=dict(DIR=ttd))
            _is_start, _is_complete = False, False

            def _start():
                nonlocal _is_start
                _is_start = True

            def _complete():
                nonlocal _is_complete
                _is_complete = True

            c(run_success=True, output_start=_start, output_complete=_complete)
            assert not _is_start
            assert not _is_complete
            assert not os.path.exists(os.path.join(ttd, 'r.md'))

        with isolated_directory({'r.md': 'README.md'}), tempfile.TemporaryDirectory() as ttd:
            c = ct(scriptdir=original_path, workdir='.', environ=dict(DIR=ttd))
            _is_start, _is_complete = False, False

            def _start():
                nonlocal _is_start
                _is_start = True

            def _complete():
                nonlocal _is_complete
                _is_complete = True

            c(run_success=False, output_start=_start, output_complete=_complete)
            assert _is_start
            assert _is_complete

            assert os.path.exists(os.path.join(ttd, 'r.md'))
            with open(os.path.join(original_path, 'README.md'), 'rb') as of, \
                    open(os.path.join(ttd, 'r.md'), 'rb') as tf:
                assert of.read() == tf.read()

    def test_call_on_all(self):
        ct = CopyFileOutputTemplate(
            local='./r.md',
            file='${DIR}/r.md',
            on_='all',
        )
        original_path = os.path.abspath('.')

        with isolated_directory({'r.md': 'README.md'}), tempfile.TemporaryDirectory() as ttd:
            c = ct(scriptdir=original_path, workdir='.', environ=dict(DIR=ttd))
            _is_start, _is_complete = False, False

            def _start():
                nonlocal _is_start
                _is_start = True

            def _complete():
                nonlocal _is_complete
                _is_complete = True

            c(run_success=True, output_start=_start, output_complete=_complete)
            assert _is_start
            assert _is_complete

            assert os.path.exists(os.path.join(original_path, 'README.md'))
            with open(os.path.join(original_path, 'README.md'), 'rb') as of, open('r.md', 'rb') as tf:
                assert of.read() == tf.read()

        with isolated_directory({'r.md': 'README.md'}), tempfile.TemporaryDirectory() as ttd:
            c = ct(scriptdir=original_path, workdir='.', environ=dict(DIR=ttd))
            _is_start, _is_complete = False, False

            def _start():
                nonlocal _is_start
                _is_start = True

            def _complete():
                nonlocal _is_complete
                _is_complete = True

            c(run_success=False, output_start=_start, output_complete=_complete)
            assert _is_start
            assert _is_complete

            assert os.path.exists(os.path.join(original_path, 'README.md'))
            with open(os.path.join(original_path, 'README.md'), 'rb') as of, open('r.md', 'rb') as tf:
                assert of.read() == tf.read()
