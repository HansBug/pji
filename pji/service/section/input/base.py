import os
from abc import ABCMeta, abstractmethod
from typing import Optional

from pysystem.models.authority.full import FileUserAuthority, FileAuthority, FileGroupAuthority, FileOtherAuthority

from ....utils import is_inner_relative_path


def _check_os_path(path: str) -> str:
    """
    check file valid or not, when valid, just process it
    :param path: original file path
    :return: normalized file path
    """
    return os.path.normpath(path)


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


def _load_privilege(privilege=None) -> Optional[FileAuthority]:
    """
    load privilege information from data
    :param privilege: raw privilege data
    :return: privilege object or None
    """
    if privilege is not None:
        try:
            _privilege = FileAuthority.loads(privilege)
        except (TypeError, ValueError):
            _privilege = FileAuthority(
                FileUserAuthority.loads(privilege),
                FileGroupAuthority.loads('---'),
                FileOtherAuthority.loads('---'),
            )
    else:
        _privilege = None

    return _privilege


class FileInputTemplate(metaclass=ABCMeta):
    @abstractmethod
    def __call__(self, *args, **kwargs) -> 'FileInput':
        raise NotImplementedError


class FileInput(metaclass=ABCMeta):
    @abstractmethod
    def __call__(self):
        raise NotImplementedError
