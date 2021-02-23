import codecs
import os
from abc import ABCMeta
from typing import Optional, Mapping

from .base import SectionInfoTemplate, SectionInfo
from ...base import _check_workdir_file, _process_environ
from ....utils import get_repr_info, env_template


class _ILocalSectionInfo(metaclass=ABCMeta):
    def __init__(self, file: str):
        """
        :param file: local path
        """
        self.__file = file

    def __repr__(self):
        """
        :return: representation string
        """
        return get_repr_info(
            cls=self.__class__,
            args=[
                ('file', lambda: repr(self.__file)),
            ]
        )


class LocalSectionInfoTemplate(SectionInfoTemplate, _ILocalSectionInfo):
    def __init__(self, file: str):
        """
        :param file: local path
        """
        self.__file = file

        _ILocalSectionInfo.__init__(self, self.__file)

    @property
    def file(self) -> str:
        return self.__file

    def __call__(self, workdir: str, environ: Optional[Mapping[str, str]] = None, **kwargs) -> 'LocalSectionInfo':
        """
        generate local info info object from extension information
        :param workdir: work directory
        :param environ: environment variable
        :return: local info info object
        """
        environ = _process_environ(environ)
        _local = os.path.normpath(
            os.path.abspath(os.path.join(workdir, _check_workdir_file(env_template(self.__file, environ)))))

        return LocalSectionInfo(file=_local)


class LocalSectionInfo(SectionInfo, _ILocalSectionInfo):
    def __init__(self, file: str):
        """
        :param file: local path
        """
        self.__file = file

        _ILocalSectionInfo.__init__(self, self.__file)

    @property
    def file(self) -> str:
        return self.__file

    def __call__(self) -> str:
        """
        execute this info info
        """
        if os.path.isdir(self.__file):
            raise IsADirectoryError('Path {path} is directory.'.format(path=repr(self.__file)))
        with codecs.open(self.__file, 'r') as file:
            return file.read()
