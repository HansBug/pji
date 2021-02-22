from enum import IntEnum, unique
from typing import Mapping, Any

from .base import FileOutputTemplate
from .copy import CopyFileOutputTemplate
from .tag import TagFileOutputTemplate


@unique
class FileOutputType(IntEnum):
    COPY = 1
    TAG = 2

    @classmethod
    def loads(cls, value) -> 'FileOutputType':
        """
        Load FileOutputType from value
        :param value: raw value
        :return: file output type object
        """
        if isinstance(value, cls):
            return value
        elif isinstance(value, str):
            if value.upper() in cls.__members__.keys():
                return cls.__members__[value.upper()]
            else:
                raise KeyError('Unknown file output type - {actual}.'.format(actual=repr(value)))
        elif isinstance(value, int):
            _mapping = {v.value: v for k, v in cls.__members__.items()}
            if value in _mapping.keys():
                return _mapping[value]
            else:
                raise ValueError('Unknown file output type value - {actual}'.format(actual=repr(value)))
        else:
            raise TypeError('Int, str or {cls} expected but {actual} found.'.format(
                cls=cls.__name__,
                actual=repr(type(value).__name__)
            ))


_TYPE_TO_TEMPLATE_CLASS = {
    FileOutputType.COPY: CopyFileOutputTemplate,
    FileOutputType.TAG: TagFileOutputTemplate,
}


# noinspection DuplicatedCode
def autoload_output_template(json: Mapping[str, Any]) -> FileOutputTemplate:
    """
    load template object from json data
    :param json: json data
    :return: file output template object
    """
    if 'type' not in json.keys():
        raise KeyError('Key {type} not found.'.format(type=repr('type')))

    _type = FileOutputType.loads(json['type'])
    _json = dict(json)
    del _json['type']

    return _TYPE_TO_TEMPLATE_CLASS[_type](**_json)
