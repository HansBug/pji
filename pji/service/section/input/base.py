from abc import ABCMeta, abstractmethod
from typing import Optional

from pysystem.models.authority.full import FileUserAuthority, FileAuthority, FileGroupAuthority, FileOtherAuthority


def _load_privilege_for_file_input(privilege=None) -> Optional[FileAuthority]:
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
