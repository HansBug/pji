import tempfile
from typing import List, Mapping, Tuple, Any, Callable

from .base import _ISection
from ..info import SectionInfoMapping
from ..input import FileInputCollection
from ..output import FileOutputCollection
from ...base import _process_environ
from ...command import CommandCollection
from ....control.model import Identification, ResourceLimit, RunResult

_DEFAULT_WORKDIR = '.'


class Section(_ISection):
    def __init__(self, name: str,
                 commands: Callable[..., CommandCollection],
                 identification: Identification, resources: ResourceLimit, environ,
                 inputs: Callable[..., FileInputCollection],
                 outputs: Callable[..., FileOutputCollection],
                 infos: Callable[..., SectionInfoMapping]):
        """
        :param name: name of section
        :param commands: command collection
        :param identification: identification
        :param resources: resource limits
        :param environ: environment variables
        :param inputs: input collection
        :param outputs: output collection
        :param infos: information collection
        """
        self.__name = name
        self.__commands = commands

        self.__identification = identification
        self.__resources = resources
        self.__environ = _process_environ(environ)

        self.__inputs = inputs
        self.__outputs = outputs
        self.__infos = infos

        _ISection.__init__(self, self.__name, self.__identification, self.__resources, self.__environ,
                           self.__inputs(workdir=_DEFAULT_WORKDIR), self.__outputs(workdir=_DEFAULT_WORKDIR),
                           self.__infos(workdir=_DEFAULT_WORKDIR), self.__commands(workdir=_DEFAULT_WORKDIR))

    @property
    def name(self) -> str:
        return self.__name

    @property
    def commands(self) -> Callable[..., CommandCollection]:
        return self.__commands

    @property
    def identification(self) -> Identification:
        return self.__identification

    @property
    def resources(self) -> ResourceLimit:
        return self.__resources

    @property
    def environ(self) -> Mapping[str, str]:
        return self.__environ

    @property
    def inputs(self) -> Callable[..., FileInputCollection]:
        return self.__inputs

    @property
    def outputs(self) -> Callable[..., FileOutputCollection]:
        return self.__outputs

    @property
    def infos(self) -> Callable[..., SectionInfoMapping]:
        return self.__infos

    def __call__(self) -> Tuple[bool, List[RunResult], Mapping[str, Any]]:
        """
        run section
        :return: success or not, result list, information
        """
        with tempfile.TemporaryDirectory() as workdir:
            self.__inputs(workdir=workdir)()
            _success, _results = self.__commands(workdir=workdir)()
            if _success:
                self.__outputs(workdir=workdir)()
            _info = self.__infos(workdir=workdir)()

            return _success, _results, _info
