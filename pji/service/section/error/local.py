import codecs
import os
from abc import ABCMeta
from typing import Optional, Mapping

from .base import ErrorInfoTemplate, ErrorInfo
from ...base import _check_workdir_path
from ....utils import get_repr_info, env_template


class _ILocalErrorInfo(metaclass=ABCMeta):
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


class LocalErrorInfoTemplate(ErrorInfoTemplate, _ILocalErrorInfo):
    def __init__(self, file: str):
        """
        :param file: local path
        """
        self.__file = file

        _ILocalErrorInfo.__init__(self, self.__file)

    @property
    def file(self) -> str:
        return self.__file

    def __call__(self, workdir: str, environ: Optional[Mapping[str, str]] = None, **kwargs) -> 'LocalErrorInfo':
        """
        generate local error info object from extension information
        :param workdir: work directory
        :param environ: environment variable
        :return: local error info object
        """
        environ = environ or {}
        _local = os.path.normpath(
            os.path.abspath(os.path.join(workdir, _check_workdir_path(env_template(self.__file, environ)))))

        return LocalErrorInfo(file=_local)


class LocalErrorInfo(ErrorInfo, _ILocalErrorInfo):
    def __init__(self, file: str):
        """
        :param file: local path
        """
        self.__file = file

        _ILocalErrorInfo.__init__(self, self.__file)

    @property
    def file(self) -> str:
        return self.__file

    def __call__(self) -> str:
        """
        execute this error info
        """
        if os.path.isdir(self.__file):
            raise IsADirectoryError('Path {path} is directory.'.format(path=repr(self.__file)))
        with codecs.open(self.__file, 'r') as file:
            return file.read()
