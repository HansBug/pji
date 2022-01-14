import codecs
import os
import tempfile

import pytest

from pji.entry.script import load_pji_script
from .scripts import DEMO_B64_SCRIPT, DEMO_B64_TEST_SCRIPT_PY, DEMO_B64_BEFORE_SCRIPT


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestEntryScript:
    def test_simple_demo(self):
        with tempfile.TemporaryDirectory() as workdir:
            with codecs.open(os.path.join(workdir, 'pscript.yml'), 'w') as sf:
                sf.write(DEMO_B64_SCRIPT)
            with codecs.open(os.path.join(workdir, 'test_script.py'), 'w') as pf:
                pf.write(DEMO_B64_TEST_SCRIPT_PY)

            _script = load_pji_script(os.path.join(workdir, 'pscript.yml'))
            _success, _result = _script('run_python')

            assert _success
            with codecs.open(os.path.join(workdir, 'test_result.txt'), 'r') as rf:
                assert rf.read().rstrip() == '5'

    def test_simple_with_dir_script(self):
        with tempfile.TemporaryDirectory() as workdir:
            with codecs.open(os.path.join(workdir, 'pscript.yml'), 'w') as sf:
                sf.write(DEMO_B64_SCRIPT)
            with codecs.open(os.path.join(workdir, 'test_script.py'), 'w') as pf:
                pf.write(DEMO_B64_TEST_SCRIPT_PY)

            _script = load_pji_script(workdir)
            _success, _result = _script('run_python')

            assert _success
            with codecs.open(os.path.join(workdir, 'test_result.txt'), 'r') as rf:
                assert rf.read().rstrip() == '5'

    def test_before_env(self):
        with tempfile.TemporaryDirectory() as workdir:
            with codecs.open(os.path.join(workdir, 'pscript.yml'), 'w') as sf:
                sf.write(DEMO_B64_BEFORE_SCRIPT)
            with codecs.open(os.path.join(workdir, 'test_script.py'), 'w') as pf:
                pf.write(DEMO_B64_TEST_SCRIPT_PY)

            _script = load_pji_script(workdir)
            _success, _result = _script('run_python', environ={'INPUT': '1 2 3 4 5 6 7'})

            assert _success
            with codecs.open(os.path.join(workdir, 'test_result.txt'), 'r') as rf:
                assert rf.read().rstrip() == '33'

    def test_after_env(self):
        with tempfile.TemporaryDirectory() as workdir:
            with codecs.open(os.path.join(workdir, 'pscript.yml'), 'w') as sf:
                sf.write(DEMO_B64_SCRIPT)
            with codecs.open(os.path.join(workdir, 'test_script.py'), 'w') as pf:
                pf.write(DEMO_B64_TEST_SCRIPT_PY)

            _script = load_pji_script(workdir)
            _success, _result = _script('run_python', environ_after={'INPUT': '1 2 3 4 5 6 7'})

            assert _success
            with codecs.open(os.path.join(workdir, 'test_result.txt'), 'r') as rf:
                assert rf.read().rstrip() == '28'
