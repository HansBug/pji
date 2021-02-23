from abc import ABCMeta
from typing import Tuple, List, Mapping

from .section import Section
from .template import SectionTemplate
from ....control.model import RunResult


class _ISectionCollection(metaclass=ABCMeta):
    def __init__(self, sections):
        self.__sections = sections


class SectionCollectionTemplate(_ISectionCollection):
    def __init__(self, *sections):
        self.__sections = [SectionTemplate.loads(item) for item in sections]
        _ISectionCollection.__init__(self, self.__sections)

    @property
    def sections(self) -> List[SectionTemplate]:
        return list(self.__sections)

    def __call__(self, **kwargs) -> 'SectionCollection':
        return SectionCollection(*[item(**kwargs) for item in self.__sections])

    @classmethod
    def loads(cls, data) -> 'SectionCollectionTemplate':
        if isinstance(data, cls):
            return data
        elif isinstance(data, SectionTemplate):
            return cls(data)
        elif isinstance(data, (list, tuple)):
            return cls(*data)
        elif isinstance(data, dict):
            return cls(data)
        else:
            raise TypeError('Array or {type} expected but {actual} found.'.format(
                type=cls.__name__, actual=repr(type(data).__name__)))


class SectionCollection(_ISectionCollection):
    def __init__(self, *sections: Section):
        self.__sections = list(sections)
        _ISectionCollection.__init__(self, self.__sections)

    @property
    def section(self) -> List[Section]:
        return list(self.__sections)

    def __call__(self) -> Tuple[bool, List[Tuple[str, Tuple[bool, List[RunResult], Mapping[str, str]]]]]:
        _success = True
        _results = []
        for section in self.__sections:
            _section_success, _section_results, _section_info = section()
            _results.append((section.name, (_section_success, _section_results, _section_info)))
            if not _section_success:
                _success = False
                break

        return _success, _results
