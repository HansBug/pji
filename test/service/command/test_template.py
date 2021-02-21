import os

import pytest

from pji.control import ResourceLimit
from pji.service.command import CommandMode, CommandTemplate


@pytest.mark.unittest
class TestServiceCommandTemplate:
    def test_simple(self):
        ct = CommandTemplate(**dict(
            args='echo 233',
        ))

        assert ct.args == 'echo 233'
        assert ct.shell
        assert ct.workdir == '.'
        assert ct.resources == ResourceLimit.loads({})
        assert ct.mode == CommandMode.COMMON
        assert ct.stdin is None
        assert ct.stdout is None
        assert ct.stderr is None

    def test_simple_2(self):
        ct = CommandTemplate(**dict(
            args='echo 233',
            shell=False,
            workdir='./123',
            resources=dict(max_real_time='2.0s'),
            mode='timing',
            stdin='stdin.txt',
            stdout='stdout.txt',
            stderr='stderr.txt',
        ))

        assert ct.args == 'echo 233'
        assert not ct.shell
        assert ct.workdir == '123'
        assert ct.resources == ResourceLimit.loads(dict(max_real_time='2.0s'))
        assert ct.mode == CommandMode.TIMING
        assert ct.stdin == 'stdin.txt'
        assert ct.stdout == 'stdout.txt'
        assert ct.stderr == 'stderr.txt'

    def test_eq(self):
        ct = CommandTemplate(**dict(
            args='echo 233'
        ))
        assert ct == ct
        assert ct == CommandTemplate(**dict(
            args='echo 233'
        ))
        assert ct != []

    def test_hash(self):
        h = {
            CommandTemplate(**dict(args='echo 233')): 1,
            CommandTemplate(**dict(args='echo 233', mode=CommandMode.MUTUAL)): 2,
        }

        assert h[CommandTemplate(**dict(args='echo 233'))] == 1
        assert h[CommandTemplate(**dict(args='echo 233', mode=CommandMode.MUTUAL))] == 2

    def test_shell_invalid(self):
        with pytest.raises(ValueError):
            CommandTemplate(
                args=['python', '-V'],
                shell=True,
            )

    def test_args_invalid(self):
        with pytest.raises(TypeError):
            CommandTemplate(args=(1, 2, 3,))

    def test_workdir_invalid(self):
        with pytest.raises(ValueError):
            CommandTemplate(args='echo 233', workdir='..')
        with pytest.raises(ValueError):
            CommandTemplate(args='echo 233', workdir='/root/1/2/3')


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
