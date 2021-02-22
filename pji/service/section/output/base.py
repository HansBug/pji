import os
from abc import ABCMeta, abstractmethod

from ....utils import is_inner_relative_path


def _check_workdir_path(path: str) -> str:
    """
    check local path valid or not, when valid, just process it
    :param path: original local path
    :return: normalized local path
    """
    if not is_inner_relative_path(path, allow_root=False):
        raise ValueError(
            'Inner relative file path expected for local but {actual} found.'.format(actual=repr(path)))
    return os.path.normpath(path)


class FileOutputTemplate(metaclass=ABCMeta):
    @abstractmethod
    def __call__(self, *args, **kwargs) -> 'FileOutput':
        raise NotImplementedError


class FileOutput(metaclass=ABCMeta):
    @abstractmethod
    def __call__(self):
        raise NotImplementedError
