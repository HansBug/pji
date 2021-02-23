from abc import ABCMeta
from typing import Mapping, Any

from .base import SectionInfoTemplate, SectionInfo
from .general import load_error_template
from ....utils import get_repr_info


class _ISectionInfoMapping(metaclass=ABCMeta):
    def __init__(self, items: Mapping[str, Any]):
        """
        :param items: mapping of section info objects
        """
        self.__items = items

    def __repr__(self):
        """
        :return: representation string
        """
        return get_repr_info(
            cls=self.__class__,
            args=[
                ('keys', lambda: repr(tuple(sorted(self.__items.keys())))),
            ]
        )


class SectionInfoMappingTemplate(_ISectionInfoMapping):
    def __init__(self, **kwargs):
        """
        :param kwargs: mapping of section info template objects
        """
        self.__items = {key: load_error_template(data) for key, data in kwargs.items()}

        _ISectionInfoMapping.__init__(self, self.__items)

    @property
    def items(self) -> Mapping[str, SectionInfoTemplate]:
        return dict(self.__items)

    def __iter__(self):
        return self.items.items().__iter__()

    def __call__(self, **kwargs) -> 'SectionInfoMapping':
        """
        get section info info mapping object
        :param kwargs: plenty of arguments
        :return: section info info mapping object
        """
        return SectionInfoMapping(**{
            key: template(**kwargs) for key, template in self.__items.items()
        })

    @classmethod
    def loads(cls, data) -> 'SectionInfoMappingTemplate':
        """
        load section info mapping template from data
        :param data: raw data
        :return: section info mapping template
        """
        if isinstance(data, cls):
            return data
        elif isinstance(data, dict):
            return cls(**data)
        else:
            raise TypeError('Json or {type} expected but {actual} found.'.format(
                type=cls.__name__, actual=repr(type(data).__name__)))


class SectionInfoMapping(_ISectionInfoMapping):
    def __init__(self, **kwargs):
        """
        :param kwargs: mapping of section info objects
        """
        self.__items = kwargs

        _ISectionInfoMapping.__init__(self, self.__items)

    @property
    def items(self) -> Mapping[str, SectionInfo]:
        return dict(self.__items)

    def __iter__(self):
        return self.items.items().__iter__()

    def __call__(self) -> Mapping[str, Any]:
        """
        execute this info info
        """
        return {key: info() for key, info in self.__items.items()}
