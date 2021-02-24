from abc import ABCMeta
from functools import partial
from typing import Tuple, List, Mapping, Callable

from .section import Section
from .template import SectionTemplate
from ....control.model import RunResult
from ....utils import get_repr_info, FilePool, duplicates


class _ISectionCollection(metaclass=ABCMeta):
    def __init__(self, items):
        """
        :param items: list of sections
        """
        self.__items = items

    def __repr__(self):
        """
        :return: get representation string
        """
        return get_repr_info(
            cls=self.__class__,
            args=[
                ('sections', lambda: repr(tuple(section.name for section in self.__items))),
            ]
        )


_SECTION_GETTER = Callable[..., Section]


class SectionCollectionTemplate(_ISectionCollection):
    def __init__(self, *items):
        """
        :param items: section templates
        """
        self.__items = [SectionTemplate.loads(item) for item in items]
        _ISectionCollection.__init__(self, self.__items)

    @property
    def items(self) -> List[SectionTemplate]:
        return list(self.__items)

    def __iter__(self):
        return self.items.__iter__()

    def __call__(self, scriptdir: str, identification=None, resources=None, environ=None,
                 **kwargs) -> 'SectionCollection':
        """
        generate section collection object
        :param scriptdir: script directory
        :param identification: identification
        :param resources: resource limits
        :param environ: environment variables
        :param kwargs: any other arguments
        :return: section collection object
        """
        if 'pool' in kwargs.keys():
            raise KeyError('Pool is not allowed to pass into section collection template.')

        _section_getters = [partial(
            item,
            scriptdir=scriptdir,
            identification=identification,
            resources=resources,
            environ=environ,
        ) for item in self.__items]

        _duplicated_names = duplicates([_getter().name for _getter in _section_getters])
        if _duplicated_names:
            raise KeyError('Duplicate names - {names}.'.format(names=repr(tuple(_duplicated_names))))

        return SectionCollection(*_section_getters)

    @classmethod
    def loads(cls, data) -> 'SectionCollectionTemplate':
        """
        load section collection template from data
        :param data: raw data
        :return: section collection template object
        """
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
    def __init__(self, *getters: _SECTION_GETTER):
        """
        :param getters: functions to get section
        """
        self.__getters = list(getters)
        _ISectionCollection.__init__(self, [item() for item in self.__getters])

    @property
    def getters(self) -> List[_SECTION_GETTER]:
        return list(self.__getters)

    def __iter__(self):
        return self.getters.__iter__()

    def __call__(self) -> Tuple[bool, List[Tuple[str, Tuple[bool, List[RunResult], Mapping[str, str]]]]]:
        """
        execute this section collection
        :return: success or not, full sections result
        """
        with FilePool() as pool:
            _success = True
            _results = []
            for section_getter in self.__getters:
                section = section_getter(pool=pool)
                _section_success, _section_results, _section_info = section()
                _results.append((section.name, (_section_success, _section_results, _section_info)))
                if not _section_success:
                    _success = False
                    break

            return _success, _results
