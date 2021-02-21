import os
from typing import Union, List, Optional

from .base import _ICommandBase, CommandMode
from .command import Command
from ...control.model import ResourceLimit, Identification
from ...utils import is_inner_relative_path


class CommandTemplate(_ICommandBase):
    __DEFAULT_WORKDIR = '.'
    __DEFAULT_MODE = CommandMode.COMMON

    def __init__(self, args: Union[str, List[str]], shell: bool = True,
                 workdir: Optional[str] = None, resources=None,
                 mode=None, stdin=None, stdout=None, stderr=None):
        if not isinstance(args, (str, list)):
            raise TypeError('Args should be str or list but {actual} found.'.format(actual=repr(type(args).__name__)))
        if shell and not isinstance(args, str):
            raise ValueError(
                'Args should be string when shell is true but {actual} found.'.format(actual=repr(type(args).__name__)))
        self.__args = args
        self.__shell = shell

        workdir = os.path.normpath(str(workdir or self.__DEFAULT_WORKDIR))
        if not is_inner_relative_path(workdir):
            raise ValueError('Workdir should be inner relative path but {actual} found.'.format(actual=repr(workdir)))
        self.__workdir = workdir
        self.__resources = ResourceLimit.loads(resources or {})

        self.__mode = CommandMode.loads(mode or self.__DEFAULT_MODE)
        self.__stdin = stdin
        self.__stdout = stdout
        self.__stderr = stderr

        _ICommandBase.__init__(self, self.__args, self.__shell, self.__workdir,
                               None, self.__resources, self.__mode)

    @property
    def args(self) -> Union[str, List[str]]:
        return self.__args

    @property
    def shell(self) -> bool:
        return self.__shell

    @property
    def workdir(self) -> str:
        return self.__workdir

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

    def __tuple(self):
        return self.__args, self.__shell, self.__workdir, self.__resources, \
               self.__mode, self.__stdin, self.__stdout, self.__stdout

    def __eq__(self, other):
        if other is self:
            return True
        elif isinstance(other, self.__class__):
            return self.__tuple() == other.__tuple()
        else:
            return False

    def __hash__(self):
        return hash(self.__tuple())

    def __call__(self, identification=None, resources=None, workdir=None, environ=None) -> Command:
        _identification = Identification.loads(identification or {})
        _resources = ResourceLimit.merge(ResourceLimit.loads(resources or {}), self.__resources)
        _workdir = os.path.normpath(os.path.join(workdir or '.', self.__workdir))
        _environ = {key: str(value) for key, value in (environ or {}).items()}

        return Command(
            args=self.__args, shell=self.__shell,
            workdir=_workdir, environ=_environ,
            identification=_identification, resources=_resources,
            mode=self.__mode, stdin=self.__stdin,
            stdout=self.__stdout, stderr=self.__stderr,
        )
