import os
from typing import Optional, Mapping

from pysystem import FileAuthority, chmod

from .base import FileInputTemplate, FileInput, _load_privilege_for_file_input
from ....utils import is_inner_relative_path, auto_copy_file, get_repr_info, env_template


class _ICopyFileInput:
    def __init__(self, file: str, local: str, privilege):
        self.__file = file
        self.__local = local
        self.__privilege = privilege

    def __repr__(self):
        return get_repr_info(
            cls=self.__class__,
            args=[
                ('file', lambda: repr(self.__file)),
                ('local', lambda: repr(self.__local)),
                ('privilege', lambda: repr(self.__privilege.sign), lambda: self.__privilege is not None),
            ]
        )


def _check_file(file: str, template: bool = False) -> str:
    if template:
        return file
    else:
        return os.path.normpath(file)


def _check_local(local: str, template: bool = False, relative: bool = True) -> str:
    if relative:
        if not is_inner_relative_path(local, allow_root=False):
            raise ValueError(
                'Inner relative file path expected for local but {actual} found.'.format(actual=repr(local)))
    if template:
        return local
    else:
        return os.path.normpath(local)


class CopyFileInputTemplate(FileInputTemplate, _ICopyFileInput):
    def __init__(self, file: str, local: str, privilege=None):
        self.__file = _check_file(file, template=True)
        self.__local = _check_local(local, relative=True, template=True)
        self.__privilege = _load_privilege_for_file_input(privilege)

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
        environ = environ or {}
        _file = os.path.normpath(os.path.join(scriptdir, env_template(self.__file, environ)))
        _local = os.path.normpath(os.path.join(workdir, env_template(self.__local, environ)))

        return CopyFileInput(
            file=_file, local=_local,
            privilege=self.__privilege,
        )


class CopyFileInput(FileInput, _ICopyFileInput):
    def __init__(self, file: str, local: str, privilege: Optional[FileAuthority]):
        self.__file = _check_file(file)
        self.__local = _check_local(local, relative=False)
        self.__privilege = _load_privilege_for_file_input(privilege)

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
        auto_copy_file(self.__file, self.__local)
        if self.__privilege is not None:
            chmod(self.__local, self.__privilege, recursive=True)
