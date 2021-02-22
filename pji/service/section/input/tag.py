import os
from abc import ABCMeta
from typing import Optional, Mapping

from pysystem import FileAuthority

from .base import FileInput, FileInputTemplate, _load_privilege, _apply_privilege_and_identification
from ...base import _check_workdir_file, _check_pool_tag
from ....control.model import Identification
from ....utils import get_repr_info, FilePool, env_template


class _ITagFileInput(metaclass=ABCMeta):
    def __init__(self, tag: str, local: str, privilege):
        """
        :param tag: pool tag
        :param local: local path
        :param privilege: local path privilege
        """
        self.__tag = tag
        self.__local = local
        self.__privilege = privilege

    def __repr__(self):
        """
        :return: representation string
        """
        return get_repr_info(
            cls=self.__class__,
            args=[
                ('tag', lambda: repr(self.__tag)),
                ('local', lambda: repr(self.__local)),
                ('privilege', lambda: repr(self.__privilege.sign), lambda: self.__privilege is not None),
            ]
        )


class TagFileInputTemplate(FileInputTemplate, _ITagFileInput):
    def __init__(self, tag: str, local: str, privilege=None):
        """
        :param tag: pool tag
        :param local: local path
        :param privilege: local path privilege
        """
        self.__tag = tag
        self.__local = local
        self.__privilege = _load_privilege(privilege)

        _ITagFileInput.__init__(self, self.__tag, self.__local, self.__privilege)

    @property
    def tag(self) -> str:
        return self.__tag

    @property
    def local(self) -> str:
        return self.__local

    @property
    def privilege(self) -> Optional[FileAuthority]:
        return self.__privilege

    def __call__(self, workdir: str, pool: FilePool, identification=None,
                 environ: Optional[Mapping[str, str]] = None, **kwargs) -> 'TagFileInput':
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
        _identification = Identification.loads(identification)

        return TagFileInput(
            pool=pool, tag=_tag, local=_local,
            privilege=self.__privilege,
            identification=_identification,
        )


class TagFileInput(FileInput, _ITagFileInput):
    def __init__(self, pool: FilePool, tag: str, local: str,
                 privilege: Optional[FileAuthority],
                 identification: Optional[Identification]):
        """
        :param pool: file pool
        :param tag: pool tag
        :param local: local path
        :param privilege: local path privilege
        """
        self.__pool = pool
        self.__tag = tag
        self.__local = local
        self.__privilege = privilege
        self.__identification = identification

        _ITagFileInput.__init__(self, self.__tag, self.__local, self.__privilege)

    @property
    def tag(self) -> str:
        return self.__tag

    @property
    def local(self) -> str:
        return self.__local

    @property
    def privilege(self) -> Optional[FileAuthority]:
        return self.__privilege

    def __call__(self):
        """
        execute this file input
        """
        self.__pool.export(self.__tag, self.__local)
        _apply_privilege_and_identification(self.__local, self.__privilege, self.__identification)
