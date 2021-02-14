from typing import Optional, Tuple

from pysystem import SystemUser, SystemGroup


def users_load(user=None, group=None) -> Tuple[Optional[SystemUser], Optional[SystemGroup]]:
    if user is not None:
        user = SystemUser.loads(user)
        group = SystemGroup.loads(group or user.primary_group)
    elif group is not None:
        user = None
        group = SystemGroup.loads(group)
    else:
        user = None
        group = None

    return user, group


def users_apply(user=None, group=None):
    user, group = users_load(user, group)
    if group is not None:
        group.apply()
    if user is not None:
        user.apply(include_group=False)
