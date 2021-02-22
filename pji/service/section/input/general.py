from enum import IntEnum, unique
from typing import Mapping, Any

from .base import FileInputTemplate
from .copy import CopyFileInputTemplate
from .link import LinkFileInputTemplate
from .tag import TagFileInputTemplate


@unique
class FileInputType(IntEnum):
    COPY = 1
    LINK = 2
    TAG = 3

    @classmethod
    def loads(cls, value) -> 'FileInputType':
        """
        Load FileInputType from value
        :param value: raw value
        :return: file input type object
        """
        if isinstance(value, cls):
            return value
        elif isinstance(value, str):
            if value.upper() in cls.__members__.keys():
                return cls.__members__[value.upper()]
            else:
                raise KeyError('Unknown file input type - {actual}.'.format(actual=repr(value)))
        elif isinstance(value, int):
            _mapping = {v.value: v for k, v in cls.__members__.items()}
            if value in _mapping.keys():
                return _mapping[value]
            else:
                raise ValueError('Unknown file input type value - {actual}'.format(actual=repr(value)))
        else:
            raise TypeError('Int, str or {cls} expected but {actual} found.'.format(
                cls=cls.__name__,
                actual=repr(type(value).__name__)
            ))


_TYPE_TO_TEMPLATE_CLASS = {
    FileInputType.COPY: CopyFileInputTemplate,
    FileInputType.LINK: LinkFileInputTemplate,
    FileInputType.TAG: TagFileInputTemplate,
}


def autoload_template(json: Mapping[str, Any]) -> FileInputTemplate:
    """
    load template object from json data
    :param json: json data
    :return: file input template object
    """

    if 'type' not in json.keys():
        raise KeyError('Key {type} not found.'.format(type=repr('type')))

    _type = FileInputType.loads(json['type'])
    _json = dict(json)
    del _json['type']

    return _TYPE_TO_TEMPLATE_CLASS[_type](**_json)
