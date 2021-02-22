from typing import Optional, Mapping

from .base import ErrorInfoTemplate, ErrorInfo
from ....utils import get_repr_info, env_template


class _IStaticErrorInfo:
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


class StaticErrorInfoTemplate(ErrorInfoTemplate, _IStaticErrorInfo):
    def __init__(self, value: str):
        """
        :param value: static value 
        """
        self.__value = value
        _IStaticErrorInfo.__init__(self, self.__value)

    @property
    def value(self):
        return self.__value

    def __call__(self, environ: Optional[Mapping[str, str]] = None) -> 'StaticErrorInfo':
        """
        get static error info object
        :param environ: environment variables
        :return: static error info object
        """
        environ = environ or {}
        if isinstance(self.__value, str):
            _value = env_template(self.__value, environ)
        else:
            _value = self.__value

        return StaticErrorInfo(value=_value)


class StaticErrorInfo(ErrorInfo, _IStaticErrorInfo):
    def __init__(self, value: str):
        """
        :param value: static value 
        """
        self.__value = value
        _IStaticErrorInfo.__init__(self, self.__value)

    @property
    def value(self):
        return self.__value

    def __call__(self):
        """
        execute this error info
        """
        return self.__value
