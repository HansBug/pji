from functools import reduce
from typing import Mapping, Union, Optional

from pysystem import SystemUser, SystemGroup


class Identification:
    def __init__(self, user=None, group=None, auto_group: bool = False):
        if user is not None:
            self.__user = SystemUser.loads(user)
        else:
            self.__user = None

        if group is not None:
            self.__group = SystemGroup.loads(group)
        elif auto_group and self.__user is not None:
            self.__group = self.__user.primary_group
        else:
            self.__group = None

    @property
    def user(self) -> SystemUser:
        return self.__user

    @property
    def group(self) -> SystemGroup:
        return self.__group

    def to_json(self) -> Mapping[str, Optional[Union[SystemUser, SystemGroup]]]:
        return {
            'user': self.user.name if self.user else None,
            'group': self.group.name if self.group else None,
        }

    @classmethod
    def loads(cls, data) -> 'Identification':
        if isinstance(data, Identification):
            return data
        elif isinstance(data, dict):
            return cls(
                user=data.get('user', None),
                group=data.get('group', None),
                auto_group=False,
            )
        elif isinstance(data, tuple):
            _user, _group = data
            return cls(user=_user, group=_group, auto_group=False)
        elif isinstance(data, SystemUser):
            return cls(user=data, auto_group=True)
        elif isinstance(data, SystemGroup):
            return cls(user=None, group=data)
        else:
            raise ValueError('Unrecognized {actual} value for {cls}.'.format(
                actual=repr(type(data)),
                cls=repr(cls),
            ))

    @classmethod
    def merge(cls, *commands: 'Identification') -> 'Identification':
        def _merge(a: 'Identification', b: 'Identification') -> 'Identification':
            return cls(
                user=b.user or a.user,
                group=b.group or a.group,
            )

        # noinspection PyTypeChecker
        return reduce(_merge, commands, cls())
