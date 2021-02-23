import tempfile
from typing import List, Mapping, Tuple, Any, Callable

from pysystem import chown, chmod

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
                 commands_getter: Callable[..., CommandCollection],
                 identification: Identification, resources: ResourceLimit, environ,
                 inputs_getter: Callable[..., FileInputCollection],
                 outputs_getter: Callable[..., FileOutputCollection],
                 infos_getter: Callable[..., SectionInfoMapping]):
        """
        :param name: name of section
        :param commands_getter: command collection getter
        :param identification: identification
        :param resources: resource limits
        :param environ: environment variables
        :param inputs_getter: input collection getter
        :param outputs_getter: output collection getter
        :param infos_getter: information collection getter
        """
        self.__name = name
        self.__commands_getter = commands_getter

        self.__identification = identification
        self.__resources = resources
        self.__environ = _process_environ(environ)

        self.__inputs_getter = inputs_getter
        self.__outputs_getter = outputs_getter
        self.__infos_getter = infos_getter

        _ISection.__init__(self, self.__name, self.__identification,
                           self.__resources, self.__environ,
                           self.__inputs_getter(workdir=_DEFAULT_WORKDIR),
                           self.__outputs_getter(workdir=_DEFAULT_WORKDIR),
                           self.__infos_getter(workdir=_DEFAULT_WORKDIR),
                           self.__commands_getter(workdir=_DEFAULT_WORKDIR))

    @property
    def name(self) -> str:
        return self.__name

    @property
    def commands_getter(self) -> Callable[..., CommandCollection]:
        return self.__commands_getter

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
    def inputs_getter(self) -> Callable[..., FileInputCollection]:
        return self.__inputs_getter

    @property
    def outputs_getter(self) -> Callable[..., FileOutputCollection]:
        return self.__outputs_getter

    @property
    def infos_getter(self) -> Callable[..., SectionInfoMapping]:
        return self.__infos_getter

    def __call__(self) -> Tuple[bool, List[RunResult], Mapping[str, Any]]:
        """
        run section
        :return: success or not, result list, information
        """
        with tempfile.TemporaryDirectory() as workdir:
            chmod(workdir, 'r-x------')
            if self.__identification:
                chown(workdir, user=self.__identification.user, group=self.__identification.group)

            self.__inputs_getter(workdir=workdir)()
            _success, _results = self.__commands_getter(workdir=workdir)()
            if _success:
                self.__outputs_getter(workdir=workdir)()
            _info = self.__infos_getter(workdir=workdir)()

            return _success, _results, _info
