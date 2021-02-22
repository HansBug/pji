import codecs
import io
import os
import tempfile

import pytest

from pji.control import ResourceLimit, Identification, MutualStdout, MutualStderr
from pji.service.command import CommandTemplate, Command, CommandMode


def _mutual_func():
    from sys import stderr
    print('echo 233')
    print(input(), file=stderr)
    print('echo 2334 1>&2')


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestServiceCommandCommand:
    def test_template_call(self):
        ct = CommandTemplate(**dict(
            args='echo 233',
            shell=False,
            workdir='./123',
            resources=dict(max_real_time='2.0s', max_cpu_time='1.0s'),
            mode='timing',
            stdin='stdin${PATH}.txt',
            stdout='stdout${PATH}.txt',
            stderr='stderr${PATH}.txt',
        ))

        c = ct(identification='nobody', resources=dict(max_real_time='1.0s', max_cpu_time='2.0s'), workdir='./123',
               environ={'PATH': '233'})

        assert isinstance(c, Command)
        assert c.args == 'echo 233'
        assert not c.shell
        assert c.workdir == '123/123'
        assert c.resources == ResourceLimit.loads(dict(max_real_time='1.0s', max_cpu_time='1.0s'))
        assert c.identification == Identification.loads('nobody')
        assert c.environ == {'PATH': '233'}
        assert c.mode == CommandMode.TIMING
        assert c.stdin == '123/123/stdin233.txt'
        assert c.stdout == '123/123/stdout233.txt'
        assert c.stderr == '123/123/stderr233.txt'

    def test_common_with_stream(self):
        with io.StringIO("echo 233\necho 2334 1>&2") as sin, \
                io.StringIO() as sout, \
                io.StringIO() as serr:
            ct = CommandTemplate(
                args='sh',
                mode=CommandMode.COMMON,
                stdin=sin,
                stdout=sout,
                stderr=serr,
            )
            c = ct()

            result = c()
            assert result.ok

            assert sout.getvalue().rstrip() == '233'
            assert serr.getvalue().rstrip() == '2334'

    def test_common_with_input(self):
        with tempfile.NamedTemporaryFile() as fin, \
                tempfile.NamedTemporaryFile() as fout, \
                tempfile.NamedTemporaryFile() as ferr:
            with codecs.open(fin.name, 'w') as ff:
                ff.write("echo 233\necho 2334 1>&2")

            ct = CommandTemplate(
                args='sh',
                mode=CommandMode.COMMON,
                stdin=fin.name,
                stdout=fout.name,
                stderr=ferr.name,
            )
            c = ct()

            result = c()
            assert result.ok

            with codecs.open(fout.name, 'r') as ff:
                assert ff.read().rstrip() == '233'
            with codecs.open(ferr.name, 'r') as ff:
                assert ff.read().rstrip() == '2334'

    def test_timing(self):
        with tempfile.NamedTemporaryFile() as fin, \
                tempfile.NamedTemporaryFile() as fout, \
                tempfile.NamedTemporaryFile() as ferr:
            with codecs.open(fin.name, 'w') as ff:
                ff.write("""
[0.0]echo 233
[1.0]echo 2334 1>&2
                """)

            ct = CommandTemplate(
                args='sh',
                mode=CommandMode.TIMING,
                stdin=fin.name,
                stdout=fout.name,
                stderr=ferr.name,
            )
            c = ct()

            result = c()
            assert result.ok

            with codecs.open(fout.name, 'r') as ff:
                _stdout = MutualStdout.load(ff)
                assert len(_stdout.lines) == 1
                assert _stdout.str_lines[0][1].rstrip() == '233'
            with codecs.open(ferr.name, 'r') as ff:
                _stderr = MutualStderr.load(ff)
                assert len(_stderr.lines) == 1
                assert _stderr.str_lines[0][1].rstrip() == '2334'

    def test_mutual_with_string_func(self):
        with tempfile.NamedTemporaryFile() as fout, \
                tempfile.NamedTemporaryFile() as ferr:
            ct = CommandTemplate(
                args='sh',
                mode=CommandMode.MUTUAL,
                stdin='test.service.command.test_command:_mutual_func',
                stdout=fout.name,
                stderr=ferr.name,
            )
            c = ct()

            result = c()
            assert result.ok

            with codecs.open(fout.name, 'r') as ff:
                _stdout = MutualStdout.load(ff)
                assert len(_stdout.lines) == 1
                assert _stdout.str_lines[0][1].rstrip() == '233'
            with codecs.open(ferr.name, 'r') as ff:
                _stderr = MutualStderr.load(ff)
                assert len(_stderr.lines) == 1
                assert _stderr.str_lines[0][1].rstrip() == '2334'

    def test_mutual_with_func(self):
        with tempfile.NamedTemporaryFile() as fout, \
                tempfile.NamedTemporaryFile() as ferr:
            ct = CommandTemplate(
                args='sh',
                mode=CommandMode.MUTUAL,
                stdin=_mutual_func,
                stdout=fout.name,
                stderr=ferr.name,
            )
            c = ct()

            result = c()
            assert result.ok

            with codecs.open(fout.name, 'r') as ff:
                _stdout = MutualStdout.load(ff)
                assert len(_stdout.lines) == 1
                assert _stdout.str_lines[0][1].rstrip() == '233'
            with codecs.open(ferr.name, 'r') as ff:
                _stderr = MutualStderr.load(ff)
                assert len(_stderr.lines) == 1
                assert _stderr.str_lines[0][1].rstrip() == '2334'

    def test_repr(self):
        ct = CommandTemplate(**dict(
            args='echo 233 ' * 100,
            shell=False,
            workdir='./123',
            resources=dict(max_real_time='2.0s', max_cpu_time='1.0s'),
            mode='timing',
            stdin='stdin.txt',
            stdout='stdout.txt',
            stderr='stderr.txt',
        ))
        c = ct(identification='nobody', resources=dict(max_real_time='1.0s', max_cpu_time='2.0s'), workdir='./123',
               environ={'PATH': '233'})

        assert repr(c) == "<Command args: 'echo 233 echo ..(902 chars).. o 233 echo 233 ', shell: False, " \
                          "mode: TIMING, workdir: '123/123', identification: <Identification user: nobody, " \
                          "group: nogroup>, resources: <ResourceLimit cpu time: 1.000s, real time: 1.000s>>"


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
