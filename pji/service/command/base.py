import os
from enum import unique, IntEnum
from textwrap import shorten
from typing import Union, List, Optional

from ...control.model import ResourceLimit, Identification
from ...utils import get_repr_info


@unique
class CommandMode(IntEnum):
    COMMON = 1
    TIMING = 2
    MUTUAL = 3

    @classmethod
    def loads(cls, value) -> 'CommandMode':
        if isinstance(value, cls):
            return value
        elif isinstance(value, str):
            if value.upper() in cls.__members__.keys():
                return cls.__members__[value.upper()]
            else:
                raise KeyError('Unknown command mode - {actual}.'.format(actual=repr(value)))
        elif isinstance(value, int):
            _mapping = {v.value: v for k, v in CommandMode.__members__.items()}
            if value in _mapping.keys():
                return _mapping[value]
            else:
                raise ValueError('Unknown command mode value - {actual}'.format(actual=repr(value)))
        else:
            raise TypeError('Int, str or {cls} expected but {actual} found.'.format(
                cls=cls.__name__,
                actual=repr(type(value).__name__)
            ))


class _ICommand:
    def __init__(self, args: Union[str, List[str]], shell: bool = True, workdir: Optional[str] = None,
                 identification=None, resources=None, mode=None):
        self.__args = args
        self.__shell = shell
        self.__workdir = workdir
        self.__identification = identification
        self.__resources = resources
        self.__mode = mode

    def __repr__(self):
        return get_repr_info(
            cls=self.__class__,
            args=[
                ('args', lambda: shorten(repr(self.__args), width=32)),
                ('shell', lambda: repr(self.__shell), lambda: self.__shell),
                ('mode', lambda: self.__mode.name),
                ('workdir', lambda: self.__workdir,
                 lambda: os.path.normpath(self.__workdir) != os.path.normpath('.')),
                ('identification', lambda: shorten(repr(self.__identification), width=32),
                 lambda: self.__identification != Identification.loads({})),
                ('resources', lambda: shorten(repr(self.__resources), width=32),
                 lambda: self.__resources != ResourceLimit.loads({})),
            ]
        )
