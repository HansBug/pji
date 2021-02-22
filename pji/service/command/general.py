from abc import ABCMeta
from typing import List, Tuple

from .command import Command
from .template import CommandTemplate
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
        return CommandCollection(*[item(
            identification, resources, workdir, environ, **kwargs
        ) for item in self.__commands])

    @classmethod
    def loads(cls, data) -> 'CommandCollectionTemplate':
        """
        load command collection template from data
        :param data: raw data
        :return: command collection template object
        """
        if isinstance(data, CommandCollectionTemplate):
            return data
        elif isinstance(data, CommandTemplate):
            return CommandCollectionTemplate(data)
        elif isinstance(data, (list, tuple)):
            return CommandCollectionTemplate(*data)
        else:
            raise TypeError('List or {type} expected but {actual} found.'.format(
                type=CommandCollectionTemplate.__name__, actual=repr(type(data).__name__)))


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
