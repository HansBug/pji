from functools import partial
from typing import Mapping

from .base import _ISection, _check_section_name
from .section import Section
from ..info import SectionInfoMappingTemplate
from ..input import FileInputCollectionTemplate
from ..output import FileOutputCollectionTemplate
from ...base import _process_environ
from ...command import CommandCollectionTemplate
from ....control.model import Identification, ResourceLimit
from ....utils import env_template, FilePool


class SectionTemplate(_ISection):
    def __init__(self, name: str, commands,
                 identification=None, resources=None, environ=None,
                 inputs=None, outputs=None, infos=None):
        """
        :param name: section name
        :param commands: commands
        :param identification: identification
        :param resources: resource limits
        :param environ: environment variables (${ENV} supported)
        :param inputs: input collection template
        :param outputs: output collection template
        :param infos: information collection template
        """
        self.__name = name
        self.__commands = CommandCollectionTemplate.loads(commands)

        self.__identification = Identification.loads(identification)
        self.__resources = ResourceLimit.loads(resources)
        self.__environ = _process_environ(environ)

        self.__inputs = FileInputCollectionTemplate.loads(inputs)
        self.__outputs = FileOutputCollectionTemplate.loads(outputs)
        self.__infos = SectionInfoMappingTemplate.loads(infos)

        _ISection.__init__(self, self.__name, self.__identification, self.__resources,
                           self.__environ, self.__inputs, self.__outputs, self.__infos, self.__commands)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def commands(self) -> CommandCollectionTemplate:
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
    def inputs(self) -> FileInputCollectionTemplate:
        return self.__inputs

    @property
    def outputs(self) -> FileOutputCollectionTemplate:
        return self.__outputs

    @property
    def infos(self) -> SectionInfoMappingTemplate:
        return self.__infos

    def __call__(self, scriptdir: str, pool: FilePool,
                 identification=None, resources=None, environ=None, **kwargs) -> Section:
        """
        generate section object
        :param identification: identification
        :param resources: resource limits
        :param environ: environment variables
        :param kwargs: any other arguments
        :return: section object
        """
        if 'workdir' in kwargs.keys():
            raise KeyError('Workdir is not allowed to pass into section template.')

        environ = _process_environ(self.__environ, environ, enable_ext=True)
        _identification = Identification.merge(Identification.loads(identification), self.__identification)
        _resources = ResourceLimit.merge(ResourceLimit.loads(resources), self.__resources)

        arguments = dict(kwargs)
        arguments.update(
            scriptdir=scriptdir,
            pool=pool,
            environ=environ,
            identification=_identification,
            resources=_resources,
        )

        return Section(
            name=_check_section_name(env_template(self.__name, environ)),
            identification=_identification, resources=_resources, environ=environ,
            commands_getter=partial(self.__commands, **arguments),
            inputs_getter=partial(self.__inputs, **arguments),
            outputs_getter=partial(self.__outputs, **arguments),
            infos_getter=partial(self.__infos, **arguments),
        )

    @classmethod
    def loads(cls, data) -> 'SectionTemplate':
        """
        load section template from data
        :param data: raw data
        :return: section template object
        """
        if isinstance(data, cls):
            return data
        elif isinstance(data, dict):
            return cls(**data)
        else:
            raise TypeError('Json or {type} expected but {actual} found.'.format(
                type=cls.__name__, actual=repr(type(data).__name__)))
