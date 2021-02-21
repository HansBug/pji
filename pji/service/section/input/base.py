import os
from abc import ABCMeta, abstractmethod
from typing import Optional

from pysystem import chown, chmod
from pysystem.models.authority.full import FileUserAuthority, FileAuthority, FileGroupAuthority, FileOtherAuthority

from ....control.model import Identification
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


def _apply_privilege_and_identification(filename: str, privilege=None, identification=None):
    """
    Apply privilege and identification for file
    :param filename: file path
    :param privilege: file privilege
    :param identification: file identification
    """
    if privilege is not None:
        chmod(filename, privilege, recursive=True)
    if identification is not None:
        _ident = Identification.merge(Identification.load_from_file(filename), identification)
        chown(filename, _ident.user, _ident.group, recursive=True)


class FileInputTemplate(metaclass=ABCMeta):
    @abstractmethod
    def __call__(self, *args, **kwargs) -> 'FileInput':
        raise NotImplementedError


class FileInput(metaclass=ABCMeta):
    @abstractmethod
    def __call__(self):
        raise NotImplementedError
