from typing import Optional

from ..model import ResourceLimit


def resources_load(limits=None) -> Optional[ResourceLimit]:
    if limits is None:
        return None
    elif isinstance(limits, ResourceLimit):
        return limits
    elif isinstance(limits, dict):
        return ResourceLimit.load_from_json(json_data=limits)
    else:
        raise TypeError('{rl} or {dict} expected, but {actual} found.'.format(
            rl=ResourceLimit.__name__,
            dict=dict.__name__,
            actual=type(limits).__name__,
        ))


def resources_apply(limits=None):
    limits = resources_load(limits)
    if limits:
        limits.apply()
