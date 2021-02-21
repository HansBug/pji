from typing import Union, List, Optional, Mapping

from .base import _ICommandBase, CommandMode
from ...control.model import ResourceLimit, Identification, RunResult
from ...control.run import common_run, timing_run, mutual_run
from ...utils import env_template, eclosing


class Command(_ICommandBase):
    def __init__(self, args: Union[str, List[str]], shell: bool,
                 workdir: Optional[str], environ: Mapping[str, str],
                 identification: Identification, resources: ResourceLimit,
                 mode, stdin, stdout, stderr):
        self.__args = args
        self.__shell = shell

        self.__environ = environ
        self.__workdir = env_template(workdir, self.__environ)

        self.__identification = identification
        self.__resources = resources

        self.__mode = mode
        self.__stdin = env_template(stdin, self.__environ) if isinstance(stdin, str) else stdin
        self.__stdout = env_template(stdout, self.__environ) if isinstance(stdout, str) else stdout
        self.__stderr = env_template(stderr, self.__environ) if isinstance(stderr, str) else stderr

        _ICommandBase.__init__(self, self.__args, self.__shell, self.__workdir,
                               self.__identification, self.__resources, self.__mode)

    @property
    def args(self) -> Union[str, List[str]]:
        return self.__args

    @property
    def shell(self) -> bool:
        return self.__shell

    @property
    def environ(self) -> Mapping[str, str]:
        return self.__environ

    @property
    def workdir(self) -> str:
        return self.__workdir

    @property
    def identification(self) -> Identification:
        return self.__identification

    @property
    def resources(self) -> ResourceLimit:
        return self.__resources

    @property
    def mode(self) -> CommandMode:
        return self.__mode

    @property
    def stdin(self):
        return self.__stdin

    @property
    def stdout(self):
        return self.__stdout

    @property
    def stderr(self):
        return self.__stderr

    __RUN_FUNCTION = {
        CommandMode.COMMON: common_run,
        CommandMode.TIMING: timing_run,
        CommandMode.MUTUAL: mutual_run,
    }

    def __call__(self) -> RunResult:
        if isinstance(self.__stdin, str) and self.__mode != CommandMode.MUTUAL:
            stdin = open(self.__stdin, 'rb', 0)
            stdin_need_close = True
        else:
            stdin = self.__stdin
            stdin_need_close = False

        if isinstance(self.__stdout, str):
            stdout = open(self.__stdout, 'wb', 0)
            stdout_need_close = True
        else:
            stdout = self.__stdout
            stdout_need_close = False

        if isinstance(self.__stderr, str):
            stderr = open(self.__stderr, 'wb', 0)
            stderr_need_close = True
        else:
            stderr = self.__stderr
            stderr_need_close = False

        with eclosing(stdin, stdin_need_close) as fstdin, \
                eclosing(stdout, stdout_need_close) as fstdout, \
                eclosing(stderr, stderr_need_close) as fstderr:

            return self.__RUN_FUNCTION[self.__mode](
                args=self.__args, shell=self.__shell,
                stdin=fstdin, stdout=fstdout, stderr=fstderr,
                environ=self.__environ, cwd=self.__workdir,
                resources=self.__resources, identification=self.__identification,
            )
