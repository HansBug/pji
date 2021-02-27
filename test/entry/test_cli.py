import codecs
import os

import pytest
from click.testing import CliRunner

from pji.entry import cli
from .scripts import DEMO_B64_SCRIPT, DEMO_B64_TEST_SCRIPT_PY


# ATTENTION: cli runner of click cannot run properly when using the cli
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
        assert "Section 'get_test_info' execute complete!" in result.output


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
