from typing import Optional, Mapping

from .base import SectionInfoTemplate, SectionInfo
from ....utils import get_repr_info, env_template


class _IStaticSectionInfo:
    def __init__(self, value: str):
        """
        :param value: static value 
        """
        self.__value = value

    def __repr__(self):
        """
        :return: representation string 
        """
        return get_repr_info(
            cls=self.__class__,
            args=[
                ('value', lambda: repr(self.__value)),
            ]
        )


class StaticSectionInfoTemplate(SectionInfoTemplate, _IStaticSectionInfo):
    def __init__(self, value: str):
        """
        :param value: static value 
        """
        self.__value = value
        _IStaticSectionInfo.__init__(self, self.__value)

    @property
    def value(self):
        return self.__value

    def __call__(self, environ: Optional[Mapping[str, str]] = None, **kwargs) -> 'StaticSectionInfo':
        """
        get static info info object
        :param environ: environment variables
        :return: static info info object
        """
        environ = environ or {}
        if isinstance(self.__value, str):
            _value = env_template(self.__value, environ)
        else:
            _value = self.__value

        return StaticSectionInfo(value=_value)


class StaticSectionInfo(SectionInfo, _IStaticSectionInfo):
    def __init__(self, value: str):
        """
        :param value: static value 
        """
        self.__value = value
        _IStaticSectionInfo.__init__(self, self.__value)

    @property
    def value(self):
        return self.__value

    def __call__(self):
        """
        execute this info info
        """
        return self.__value
