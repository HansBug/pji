import os
import tempfile

import pytest

from pji.control.model import RunResultStatus
from pji.service.command import CommandCollectionTemplate, CommandTemplate


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestServiceCommandCollection:
    def test_template(self):
        cct = CommandCollectionTemplate(
            CommandTemplate(args='echo 233'),
            CommandTemplate(args='echo 2334 1>&2 ')
        )

        assert len(cct.commands) == 2
        assert repr(cct) == "<CommandCollectionTemplate commands: 2>"

    def test_template_call(self):
        cct = CommandCollectionTemplate(
            CommandTemplate(args='echo 233'),
            CommandTemplate(args='echo 2334 1>&2 ')
        )
        cc = cct(identification='nobody', workdir='.')

        assert len(cc.commands) == 2
        assert repr(cc) == "<CommandCollection commands: 2>"

    def test_collection_execute(self):
        cct = CommandCollectionTemplate(
            CommandTemplate(args='echo 233'),
            CommandTemplate(args='echo 2334 1>&2 ')
        )
        cc = cct(identification='nobody', workdir='.')
        _success, _results = cc()
        assert _success
        assert len(_results) == 2
        assert _results[0].ok
        assert _results[1].ok

    def test_collection_with_output(self):
        cct = CommandCollectionTemplate(
            CommandTemplate(args='echo 233 ${PJI_COMMAND_INDEX}', stdout='stdout_1_${T}.txt', stderr='stderr_1_${T}.txt'),
            CommandTemplate(args='echo 2334 ${PJI_COMMAND_INDEX} 1>&2 ', stdout='stdout_2_${T}.txt',
                            stderr='stderr_2_${T}.txt'),
        )

        with tempfile.TemporaryDirectory() as wtd:
            cc = cct(identification='nobody', workdir=wtd, environ=dict(T='233'))

            assert cc.commands[0].stdout == os.path.join(wtd, 'stdout_1_233.txt')
            assert cc.commands[0].stderr == os.path.join(wtd, 'stderr_1_233.txt')
            assert cc.commands[1].stdout == os.path.join(wtd, 'stdout_2_233.txt')
            assert cc.commands[1].stderr == os.path.join(wtd, 'stderr_2_233.txt')

            _success, _results = cc()

            assert _success
            assert len(_results) == 2
            assert _results[0].ok
            assert _results[1].ok

            with open(os.path.join(wtd, 'stdout_1_233.txt'), 'r') as ff:
                assert ff.read().rstrip() == '233 0'
            with open(os.path.join(wtd, 'stderr_1_233.txt'), 'r') as ff:
                assert ff.read().rstrip() == ''
            with open(os.path.join(wtd, 'stdout_2_233.txt'), 'r') as ff:
                assert ff.read().rstrip() == ''
            with open(os.path.join(wtd, 'stderr_2_233.txt'), 'r') as ff:
                assert ff.read().rstrip() == '2334 1'

    def test_collection_with_failure(self):
        cct = CommandCollectionTemplate(
            CommandTemplate(args='echo 233', stdout='stdout_1_${T}.txt', stderr='stderr_1_${T}.txt'),
            CommandTemplate(args='echo 2334 1>&2 ', stdout='stdout_2_${T}.txt', stderr='stderr_2_${T}.txt'),
            CommandTemplate(args='false'),
        )

        with tempfile.TemporaryDirectory() as wtd:
            cc = cct(identification='nobody', workdir=wtd, environ=dict(T='233'))

            assert cc.commands[0].stdout == os.path.join(wtd, 'stdout_1_233.txt')
            assert cc.commands[0].stderr == os.path.join(wtd, 'stderr_1_233.txt')
            assert cc.commands[1].stdout == os.path.join(wtd, 'stdout_2_233.txt')
            assert cc.commands[1].stderr == os.path.join(wtd, 'stderr_2_233.txt')

            _success, _results = cc()

            assert not _success
            assert len(_results) == 3
            assert _results[0].ok
            assert _results[1].ok
            assert not _results[2].ok
            assert _results[2].status == RunResultStatus.RUNTIME_ERROR

            with open(os.path.join(wtd, 'stdout_1_233.txt'), 'r') as ff:
                assert ff.read().rstrip() == '233'
            with open(os.path.join(wtd, 'stderr_1_233.txt'), 'r') as ff:
                assert ff.read().rstrip() == ''
            with open(os.path.join(wtd, 'stdout_2_233.txt'), 'r') as ff:
                assert ff.read().rstrip() == ''
            with open(os.path.join(wtd, 'stderr_2_233.txt'), 'r') as ff:
                assert ff.read().rstrip() == '2334'

    def test_loads(self):
        cct = CommandCollectionTemplate(
            CommandTemplate(args='echo 233', stdout='stdout_1_${T}.txt', stderr='stderr_1_${T}.txt'),
            CommandTemplate(args='echo 2334 1>&2 ', stdout='stdout_2_${T}.txt', stderr='stderr_2_${T}.txt'),
            CommandTemplate(args='false'),
        )
        assert CommandCollectionTemplate.loads(cct) is cct

        assert len(CommandCollectionTemplate.loads(
            CommandTemplate(args='echo 233', stdout='stdout_1_${T}.txt', stderr='stderr_1_${T}.txt'),
        ).commands) == 1
        assert len(CommandCollectionTemplate.loads([
            CommandTemplate(args='echo 233', stdout='stdout_1_${T}.txt', stderr='stderr_1_${T}.txt'),
            CommandTemplate(args='echo 2334 1>&2 ', stdout='stdout_2_${T}.txt', stderr='stderr_2_${T}.txt'),
            CommandTemplate(args='false'),
        ]).commands) == 3
        assert len(CommandCollectionTemplate.loads(
            dict(args='echo 233', stdout='stdout_1_${T}.txt', stderr='stderr_1_${T}.txt'),
        ).commands) == 1
        with pytest.raises(TypeError):
            CommandCollectionTemplate.loads(123)


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
