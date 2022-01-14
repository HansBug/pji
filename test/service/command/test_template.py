import os
import tempfile

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
        assert ct.workdir == './123'
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
        ct = CommandTemplate(args='echo 233', workdir='..')
        with pytest.raises(ValueError):
            ct()

        ct = CommandTemplate(args='echo 233', workdir='/root/1/2/3')
        with pytest.raises(ValueError):
            ct()

    def test_loads(self):
        ct = CommandTemplate(args='echo 233')
        assert CommandTemplate.loads(ct) == ct

        ct = CommandTemplate.loads(dict(args='echo 233'))
        assert ct.args == 'echo 233'

        ct = CommandTemplate.loads('echo 233')
        assert ct.args == 'echo 233'

        ct = CommandTemplate.loads(['echo', '233'])
        assert ct.args == ['echo', '233']

    def test_loads_invalid(self):
        with pytest.raises(TypeError):
            CommandTemplate.loads(123)

    def test_run_with_stdout_stderr_1(self):
        ct = CommandTemplate(args='echo 233', stdout='stdout_1_${T}.txt', stderr='stderr_1_${T}.txt')
        with tempfile.TemporaryDirectory() as wtd:
            c = ct(identification='nobody', workdir=wtd, environ=dict(T='233'))
            c()

            with open(os.path.join(wtd, 'stdout_1_233.txt'), 'r') as ff:
                assert ff.read().rstrip() == '233'
            with open(os.path.join(wtd, 'stderr_1_233.txt'), 'r') as ff:
                assert ff.read().rstrip() == ''

    def test_run_with_stdout_stderr_2(self):
        ct = CommandTemplate(args='echo 2334 1>&2 ', stdout='stdout_2_${T}.txt', stderr='stderr_2_${T}.txt')
        with tempfile.TemporaryDirectory() as wtd:
            c = ct(identification='nobody', workdir=wtd, environ=dict(T='233'))
            c()

            with open(os.path.join(wtd, 'stdout_2_233.txt'), 'r') as ff:
                assert ff.read().rstrip() == ''
            with open(os.path.join(wtd, 'stderr_2_233.txt'), 'r') as ff:
                assert ff.read().rstrip() == '2334'
