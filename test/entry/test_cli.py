import codecs
import os

import pytest
from click.testing import CliRunner

from pji.entry.cli import cli
from .scripts import DEMO_B64_SCRIPT, DEMO_B64_TEST_SCRIPT_PY, DEMO_B64_FAIL_SCRIPT, DEMO_B64_BEFORE_SCRIPT, \
    DEMO_B64_LINK_SCRIPT


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestEntryCli:
    def test_version(self):
        runner = CliRunner()
        result = runner.invoke(cli, args=['-v'])

        assert result.exit_code == 0
        assert "pji" in result.stdout.lower()

    def test_simple_demo(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with codecs.open('pscript.yml', 'w') as sf:
                sf.write(DEMO_B64_SCRIPT)
            with codecs.open('test_script.py', 'w') as pf:
                pf.write(DEMO_B64_TEST_SCRIPT_PY)

            result = runner.invoke(cli, ['-s', 'pscript.yml', '-t', 'run_python'])

            assert result.exit_code == 0
            assert "Section 'get_test_info' execute completed!" in result.output
            assert "Section 'generate_base64' execute completed!" in result.output
            assert "Section 'run_result' execute completed!" in result.output

            with codecs.open('test_result.txt', 'r') as rf:
                assert rf.read().rstrip() == '5'

    def test_simple_with_default(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with codecs.open('pscript.yml', 'w') as sf:
                sf.write(DEMO_B64_SCRIPT)
            with codecs.open('test_script.py', 'w') as pf:
                pf.write(DEMO_B64_TEST_SCRIPT_PY)

            result = runner.invoke(cli, ['-t', 'run_python'])

            assert result.exit_code == 0
            assert "Section 'get_test_info' execute completed!" in result.output
            assert "Section 'generate_base64' execute completed!" in result.output
            assert "Section 'run_result' execute completed!" in result.output

            with codecs.open('test_result.txt', 'r') as rf:
                assert rf.read().rstrip() == '5'

    def test_simple_with_link(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with codecs.open('pscript.yml', 'w') as sf:
                sf.write(DEMO_B64_LINK_SCRIPT)
            with codecs.open('test_script.py', 'w') as pf:
                pf.write(DEMO_B64_TEST_SCRIPT_PY)

            result = runner.invoke(cli, ['-s', 'pscript.yml', '-t', 'run_python'])

            assert result.exit_code == 0
            assert "Section 'get_test_info' execute completed!" in result.output
            assert "Section 'generate_base64' execute completed!" in result.output
            assert "Section 'run_result' execute completed!" in result.output

            with codecs.open('test_result.txt', 'r') as rf:
                assert rf.read().rstrip() == '5'

    def test_before_env(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with codecs.open('pscript.yml', 'w') as sf:
                sf.write(DEMO_B64_BEFORE_SCRIPT)
            with codecs.open('test_script.py', 'w') as pf:
                pf.write(DEMO_B64_TEST_SCRIPT_PY)

            result = runner.invoke(cli, ['-s', 'pscript.yml', '-t', 'run_python', '-e', 'INPUT=1 2 3 4 5 6 7'])

            assert result.exit_code == 0
            assert "Section 'get_test_info' execute completed!" in result.output
            assert "Section 'generate_base64' execute completed!" in result.output
            assert "Section 'run_result' execute completed!" in result.output

            with codecs.open('test_result.txt', 'r') as rf:
                assert rf.read().rstrip() == '33'

    def test_after_env(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with codecs.open('pscript.yml', 'w') as sf:
                sf.write(DEMO_B64_SCRIPT)
            with codecs.open('test_script.py', 'w') as pf:
                pf.write(DEMO_B64_TEST_SCRIPT_PY)

            result = runner.invoke(cli, ['-s', 'pscript.yml', '-t', 'run_python', '-E', 'INPUT=1 2 3 4 5 6 7'])

            assert result.exit_code == 0
            assert "Section 'get_test_info' execute completed!" in result.output
            assert "Section 'generate_base64' execute completed!" in result.output
            assert "Section 'run_result' execute completed!" in result.output

            with codecs.open('test_result.txt', 'r') as rf:
                assert rf.read().rstrip() == '28'

    def test_after_fail(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with codecs.open('pscript.yml', 'w') as sf:
                sf.write(DEMO_B64_FAIL_SCRIPT)
            with codecs.open('test_script.py', 'w') as pf:
                pf.write(DEMO_B64_TEST_SCRIPT_PY)

            result = runner.invoke(cli, ['-s', 'pscript.yml', '-t', 'run_python', '-E', 'INPUT=1 2 3 4 5 6 7'])

            assert result.exit_code == 1
            assert "Section 'get_test_info' execute completed!" in result.output
            assert "Section 'generate_base64' execute completed!" in result.output
            assert "Section 'run_result' execute failed!" in result.output


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
