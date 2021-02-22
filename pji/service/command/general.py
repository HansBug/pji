from abc import ABCMeta
from typing import List, Tuple

from .command import Command
from .template import CommandTemplate
from ...control.model import RunResult
from ...utils import get_repr_info


def load_command_template(data) -> CommandTemplate:
    if isinstance(data, CommandTemplate):
        return data
    elif isinstance(data, dict):
        return CommandTemplate(**data)
    else:
        raise TypeError('Json or {type} expected but {actual} found.'.format(
            type=CommandTemplate.__name__, actual=repr(type(data).__name__)))


class _ICommandCollection(metaclass=ABCMeta):
    def __init__(self, commands):
        self.__commands = commands

    def __repr__(self):
        return get_repr_info(
            cls=self.__class__,
            args=[
                ('commands', lambda: len(self.__commands))
            ]
        )


class CommandCollectionTemplate(_ICommandCollection):
    def __init__(self, *commands: CommandTemplate):
        self.__commands = [load_command_template(item) for item in commands]

        _ICommandCollection.__init__(self, self.__commands)

    def commands(self) -> List[CommandTemplate]:
        return list(self.__commands)

    def __call__(self, identification=None, resources=None, workdir=None, environ=None) -> 'CommandCollection':
        return CommandCollection(*[item(
            identification, resources, workdir, environ,
        ) for item in self.__commands])


class CommandCollection(_ICommandCollection):
    def __init__(self, *commands: Command):
        self.__commands = commands

        _ICommandCollection.__init__(self, self.__commands)

    def commands(self) -> List[Command]:
        return list(self.__commands)

    def __call__(self) -> Tuple[bool, List[RunResult]]:
        _results = []
        for index, cmd in enumerate(self.__commands):
            result = cmd()
            _results.append(result)
            if not result.ok:
                return False, _results
        return True, _results


def load_command_template_collection(data) -> CommandCollectionTemplate:
    if isinstance(data, CommandCollectionTemplate):
        return data
    elif isinstance(data, CommandTemplate):
        return CommandCollectionTemplate(data)
    elif isinstance(data, (list, tuple)):
        return CommandCollectionTemplate(*data)
    else:
        raise TypeError('List or {type} expected but {actual} found.'.format(
            type=CommandCollectionTemplate.__name__, actual=repr(type(data).__name__)))
