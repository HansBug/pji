import codecs
import os
from functools import partial
from typing import Callable

from .runner import DispatchRunner
from ..control import RunResult
from ..service import DispatchTemplate, Dispatch, Command, FileInput, CopyFileInput, TagFileInput, LinkFileInput
from ..utils import auto_load_json, truncate


def _load_dispatch_template(filename: str) -> DispatchTemplate:
    with codecs.open(filename, 'r') as file:
        _json = auto_load_json(file)

    return DispatchTemplate.loads(_json)


class DispatchEventRunner(DispatchRunner):
    def _command_start(self, command: Command):
        _repr = truncate(repr(command.args), width=96, tail_length=24, show_length=True)
        print("Running {repr} ... ".format(repr=_repr), end='')

    def _command_complete(self, command: Command, result: RunResult):
        print(result.status.name)

    def _input_start(self, input_: FileInput):
        if isinstance(input_, CopyFileInput):
            type_ = 'diretory' if os.path.isdir(input_.file) else 'file'
            print("Coping {type} from {from_} to {to} ... ".format(type=type_, from_=repr(input_.file),
                                                                   to=repr(input_.local)), end='')
        elif isinstance(input_, TagFileInput):
            print("Loading tag {tag} to {to} ... ".format(tag=repr(input_.tag), to=repr(input_.local)), end='')
        elif isinstance(input_, LinkFileInput):
            type_ = 'diretory' if os.path.isdir(input_.file) else 'file'
            print("Linking {type} from {from_} to {to} ... ".format(type=type_, from_=repr(input_.file),
                                                                    to=repr(input_.local)), end='')

    def _input_complete(self, input_: FileInput):
        print('COMPLETE')


_DEFAULT_FILENAME = 'pscript.yml'


def _load_dispatch_getter(filename: str = None) -> Callable[..., Dispatch]:
    filename = filename or _DEFAULT_FILENAME
    _dir, _ = os.path.split(os.path.normpath(os.path.abspath(filename)))

    return partial(DispatchEventRunner(_load_dispatch_template(filename)), scriptdir=_dir)
