import os
from abc import ABCMeta
from typing import Optional, Mapping

from .base import FileInput, FileInputTemplate
from ...base import _check_workdir_file, _check_os_path
from ....utils import get_repr_info, env_template


class _ILinkFileInput(metaclass=ABCMeta):
    def __init__(self, file: str, local: str):
        """
        :param file: file path
        :param local: local path
        """
        self.__file = file
        self.__local = local

    def __repr__(self):
        """
        :return: representation string
        """
        return get_repr_info(
            cls=self.__class__,
            args=[
                ('file', lambda: repr(self.__file)),
                ('local', lambda: repr(self.__local)),
            ]
        )


class LinkFileInputTemplate(FileInputTemplate, _ILinkFileInput):
    def __init__(self, file: str, local: str):
        """
        :param file: file path
        :param local: local path
        """
        self.__file = file
        self.__local = local

        _ILinkFileInput.__init__(self, self.__file, self.__local)

    @property
    def file(self) -> str:
        return self.__file

    @property
    def local(self) -> str:
        return self.__local

    # noinspection DuplicatedCode
    def __call__(self, scriptdir: str, workdir: str,
                 environ: Optional[Mapping[str, str]] = None, **kwargs) -> 'LinkFileInput':
        """
        generate link file input object from extension information
        :param scriptdir: script directory
        :param workdir: work directory
        :param environ: environment variable
        :return: link file input object
        """
        environ = environ or {}
        _file = os.path.normpath(
            os.path.abspath(os.path.join(scriptdir, _check_os_path(env_template(self.__file, environ)))))
        _local = os.path.normpath(
            os.path.abspath(os.path.join(workdir, _check_workdir_file(env_template(self.__local, environ)))))

        return LinkFileInput(
            file=_file, local=_local,
        )


class LinkFileInput(FileInput, _ILinkFileInput):
    def __init__(self, file: str, local: str, ):
        """
        :param file: file path
        :param local: local path
        """
        self.__file = file
        self.__local = local

        _ILinkFileInput.__init__(self, self.__file, self.__local)

    @property
    def file(self) -> str:
        return self.__file

    @property
    def local(self) -> str:
        return self.__local

    def __call__(self):
        """
        execute this link event
        """
        _parent_path, _ = os.path.split(self.__local)
        os.makedirs(_parent_path, exist_ok=True)
        os.symlink(self.__file, self.__local, target_is_directory=os.path.isdir(self.__file))
