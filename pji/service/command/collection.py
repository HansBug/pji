from abc import ABCMeta
from typing import List, Tuple

from .base import ENV_PJI_COMMAND
from .command import Command
from .template import CommandTemplate
from ..base import _process_environ
from ...control.model import RunResult
from ...utils import get_repr_info


class _ICommandCollection(metaclass=ABCMeta):
    def __init__(self, commands):
        """
        :param commands: commands
        """
        self.__commands = commands

    def __repr__(self):
        """
        :return: representation string
        """
        return get_repr_info(
            cls=self.__class__,
            args=[
                ('commands', lambda: len(self.__commands))
            ]
        )


class CommandCollectionTemplate(_ICommandCollection):
    def __init__(self, *commands: CommandTemplate):
        """
        :param commands: tuple of command templates
        """
        self.__commands = [CommandTemplate.loads(item) for item in commands]

        _ICommandCollection.__init__(self, self.__commands)

    @property
    def commands(self) -> List[CommandTemplate]:
        return list(self.__commands)

    def __call__(self, identification=None, resources=None, workdir=None, environ=None,
                 **kwargs) -> 'CommandCollection':
        """
        generate command collection
        :param identification: identification
        :param resources: resource limits
        :param workdir: work directory
        :param environ: environment variables
        :return: command collection
        """
        environ = _process_environ(environ)

        def _env_with_id(index_):
            _env = dict(environ)
            _env[ENV_PJI_COMMAND] = str(index_)
            return _env

        return CommandCollection(*[item(
            identification, resources, workdir, _env_with_id(index), **kwargs
        ) for index, item in enumerate(self.__commands)])

    @classmethod
    def loads(cls, data) -> 'CommandCollectionTemplate':
        """
        load command collection template from data
        :param data: raw data
        :return: command collection template object
        """
        if isinstance(data, cls):
            return data
        elif isinstance(data, CommandTemplate):
            return cls(data)
        elif isinstance(data, (list, tuple)):
            return cls(*data)
        elif isinstance(data, dict):
            return cls(CommandTemplate.loads(data))
        else:
            raise TypeError('List or {type} expected but {actual} found.'.format(
                type=cls.__name__, actual=repr(type(data).__name__)))


class CommandCollection(_ICommandCollection):
    def __init__(self, *commands: Command):
        """
        :param commands: tuple of commands
        """
        self.__commands = commands

        _ICommandCollection.__init__(self, self.__commands)

    @property
    def commands(self) -> List[Command]:
        return list(self.__commands)

    def __call__(self) -> Tuple[bool, List[RunResult]]:
        """
        execute multiple commands one by one
        :return: success or not, list of results
        """
        _results = []
        for index, cmd in enumerate(self.__commands):
            result = cmd()
            _results.append(result)
            if not result.ok:
                return False, _results
        return True, _results
