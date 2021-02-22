import os
from typing import Optional, Mapping

from .base import FileOutputTemplate, FileOutput, _check_workdir_path
from ....utils import get_repr_info, auto_copy_file, env_template


def _check_os_path(path: str) -> str:
    """
    check file valid or not, when valid, just process it
    :param path: original file path
    :return: normalized file path
    """
    return os.path.normpath(path)


class _ICopyFileOutput:
    def __init__(self, local: str, file: str):
        """
        :param local: local path
        :param file: file path
        """
        self.__local = local
        self.__file = file

    def __repr__(self):
        """
        :return: representation string
        """

        return get_repr_info(
            cls=self.__class__,
            args=[
                ('local', lambda: repr(self.__local)),
                ('file', lambda: repr(self.__file)),
            ]
        )


class CopyFileOutputTemplate(FileOutputTemplate, _ICopyFileOutput):
    def __init__(self, local: str, file: str):
        """
        :param local: local path
        :param file: file path
        """
        self.__local = local
        self.__file = file

        _ICopyFileOutput.__init__(self, self.__local, self.__file)

    @property
    def file(self) -> str:
        return self.__file

    @property
    def local(self) -> str:
        return self.__local

    # noinspection DuplicatedCode
    def __call__(self, scriptdir: str, workdir: str, environ: Optional[Mapping[str, str]] = None,
                 **kwargs) -> 'CopyFileOutput':
        """
        generate copy file output object from extension information
        :param scriptdir: script directory
        :param workdir: work directory
        :param environ: environment variable
        :return: copy file output object
        """

        environ = environ or {}
        _local = os.path.normpath(
            os.path.abspath(os.path.join(workdir, _check_workdir_path(env_template(self.__local, environ)))))
        _file = os.path.normpath(
            os.path.abspath(os.path.join(scriptdir, _check_os_path(env_template(self.__file, environ)))))

        return CopyFileOutput(file=_file, local=_local)


class CopyFileOutput(FileOutput, _ICopyFileOutput):
    def __init__(self, local: str, file: str):
        """
        :param local: local path
        :param file: file path
        """
        self.__local = local
        self.__file = file

        _ICopyFileOutput.__init__(self, self.__local, self.__file)

    @property
    def file(self) -> str:
        return self.__file

    @property
    def local(self) -> str:
        return self.__local

    def __call__(self, *args, **kwargs):
        auto_copy_file(self.__local, self.__file)
