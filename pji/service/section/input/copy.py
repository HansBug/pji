import os
from typing import Optional, Mapping

from pysystem import FileAuthority, chmod

from .base import FileInputTemplate, FileInput, _load_privilege, _check_os_path, _check_workdir_path
from ....utils import auto_copy_file, get_repr_info, env_template


class _ICopyFileInput:
    def __init__(self, file: str, local: str, privilege):
        """
        :param file: file path
        :param local: local path
        :param privilege: local privilege
        """

        self.__file = file
        self.__local = local
        self.__privilege = privilege

    def __repr__(self):
        """
        :return: representation string
        """

        return get_repr_info(
            cls=self.__class__,
            args=[
                ('file', lambda: repr(self.__file)),
                ('local', lambda: repr(self.__local)),
                ('privilege', lambda: repr(self.__privilege.sign), lambda: self.__privilege is not None),
            ]
        )


class CopyFileInputTemplate(FileInputTemplate, _ICopyFileInput):
    def __init__(self, file: str, local: str, privilege=None):
        """
        :param file: file path
        :param local: local path
        :param privilege: local path privilege
        """
        self.__file = file
        self.__local = local
        self.__privilege = _load_privilege(privilege)

        _ICopyFileInput.__init__(self, self.__file, self.__local, self.__privilege)

    @property
    def file(self) -> str:
        return self.__file

    @property
    def local(self) -> str:
        return self.__local

    @property
    def privilege(self) -> Optional[FileAuthority]:
        return self.__privilege

    def __call__(self, scriptdir: str, workdir: str, environ: Optional[Mapping[str, str]] = None) -> 'CopyFileInput':
        """
        generate copy file input object from extension information
        :param scriptdir: script directory
        :param workdir: work directory
        :param environ: environment variable
        :return: copy file input object
        """
        environ = environ or {}
        _file = os.path.normpath(os.path.join(scriptdir, _check_os_path(env_template(self.__file, environ))))
        _local = os.path.normpath(os.path.join(workdir, _check_workdir_path(env_template(self.__local, environ))))

        return CopyFileInput(
            file=_file, local=_local,
            privilege=self.__privilege,
        )


class CopyFileInput(FileInput, _ICopyFileInput):
    def __init__(self, file: str, local: str, privilege: Optional[FileAuthority]):
        """
        :param file: file path
        :param local: local path
        :param privilege: local path privilege
        """
        self.__file = file
        self.__local = local
        self.__privilege = privilege

        _ICopyFileInput.__init__(self, self.__file, self.__local, self.__privilege)

    @property
    def file(self) -> str:
        return self.__file

    @property
    def local(self) -> str:
        return self.__local

    @property
    def privilege(self) -> Optional[FileAuthority]:
        return self.__privilege

    def __call__(self):
        """
        execute this copy event
        """
        auto_copy_file(self.__file, self.__local)
        if self.__privilege is not None:
            chmod(self.__local, self.__privilege, recursive=True)
