import os
from abc import ABCMeta
from typing import Optional, Mapping

from .base import FileOutputTemplate, FileOutput
from ...base import _check_workdir_file, _check_pool_tag
from ....utils import get_repr_info, FilePool, env_template


class _ITagFileOutput(metaclass=ABCMeta):
    def __init__(self, local: str, tag: str):
        """
        :param local: local path
        :param tag: pool tag
        """
        self.__local = local
        self.__tag = tag

    def __repr__(self):
        """
        :return: representation string
        """
        return get_repr_info(
            cls=self.__class__,
            args=[
                ('local', lambda: repr(self.__local)),
                ('tag', lambda: repr(self.__tag)),
            ]
        )


class TagFileOutputTemplate(FileOutputTemplate, _ITagFileOutput):
    def __init__(self, local: str, tag: str):
        """
        :param local: local path
        :param tag: pool tag
        """
        self.__local = local
        self.__tag = tag

        _ITagFileOutput.__init__(self, self.__local, self.__tag)

    @property
    def tag(self) -> str:
        return self.__tag

    @property
    def local(self) -> str:
        return self.__local

    def __call__(self, workdir: str, pool: FilePool,
                 environ: Optional[Mapping[str, str]] = None, **kwargs) -> 'TagFileOutput':
        """
        get tag file input object
        :param workdir: local work directory
        :param pool: file pool object
        :param environ: environment variables
        :return: tag file input object
        """
        environ = environ or {}
        _tag = _check_pool_tag(env_template(self.__tag, environ))
        _local = os.path.normpath(
            os.path.abspath(os.path.join(workdir, _check_workdir_file(env_template(self.__local, environ)))))

        return TagFileOutput(
            pool=pool, local=_local, tag=_tag,
        )


class TagFileOutput(FileOutput, _ITagFileOutput):
    def __init__(self, pool: FilePool, local: str, tag: str):
        """
        :param pool: file pool
        :param local: local path
        :param tag: pool tag
        """
        self.__pool = pool
        self.__local = local
        self.__tag = tag

        _ITagFileOutput.__init__(self, self.__local, self.__tag)

    @property
    def tag(self) -> str:
        return self.__tag

    @property
    def local(self) -> str:
        return self.__local

    def __call__(self):
        """
        execute this file output
        """
        self.__pool[self.__tag] = self.__local
