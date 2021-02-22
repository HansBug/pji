from enum import unique, IntEnum
from typing import Mapping

from .base import ErrorInfoTemplate
from .local import LocalErrorInfoTemplate
from .static import StaticErrorInfoTemplate
from .tag import TagErrorInfoTemplate


@unique
class ErrorInfoType(IntEnum):
    LOCAL = 1
    TAG = 2
    STATIC = 3

    @classmethod
    def loads(cls, value) -> 'ErrorInfoType':
        """
        Load ErrorInfoType from value
        :param value: raw value
        :return: error info type object
        """
        if isinstance(value, cls):
            return value
        elif isinstance(value, str):
            if value.upper() in cls.__members__.keys():
                return cls.__members__[value.upper()]
            else:
                raise KeyError('Unknown error info type - {actual}.'.format(actual=repr(value)))
        elif isinstance(value, int):
            _mapping = {v.value: v for k, v in cls.__members__.items()}
            if value in _mapping.keys():
                return _mapping[value]
            else:
                raise ValueError('Unknown error info type value - {actual}'.format(actual=repr(value)))
        else:
            raise TypeError('Int, str or {cls} expected but {actual} found.'.format(
                cls=cls.__name__,
                actual=repr(type(value).__name__)
            ))


# noinspection DuplicatedCode
_TYPE_TO_TEMPLATE_CLASS = {
    ErrorInfoType.LOCAL: LocalErrorInfoTemplate,
    ErrorInfoType.TAG: TagErrorInfoTemplate,
    ErrorInfoType.STATIC: StaticErrorInfoTemplate,
}


def _load_error_template_from_json(json: Mapping[str, str]) -> ErrorInfoTemplate:
    """
    load template object from json data
    :param json: json data
    :return: error info template object
    """
    if 'type' not in json.keys():
        raise KeyError('Key {type} not found.'.format(type=repr('type')))

    _type = ErrorInfoType.loads(json['type'])
    _json = dict(json)
    del _json['type']

    return _TYPE_TO_TEMPLATE_CLASS[_type](**_json)


def load_error_template(data) -> ErrorInfoTemplate:
    """
    load error info template object from data
    :param data: raw data
    :return: error info template object 
    """
    if isinstance(data, ErrorInfoTemplate):
        return data
    elif isinstance(data, dict):
        return _load_error_template_from_json(data)
    else:
        raise TypeError('Json or {type} expected but {actual} found.'.format(
            type=ErrorInfoTemplate.__name__, actual=repr(type(data).__name__)))
