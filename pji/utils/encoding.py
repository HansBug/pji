from typing import Union, Callable, TypeVar

import chardet

_ENCODING_LIST = ['utf-8', 'gbk', 'gb2312', 'gb18030', 'big5']


def auto_encode(string: str) -> bytes:
    return string.encode()


def auto_decode(data: Union[bytes, bytearray]) -> str:
    auto_encoding = chardet.detect(data)['encoding']
    if auto_encoding and auto_encoding not in _ENCODING_LIST:
        _list = _ENCODING_LIST + [auto_encoding]
    else:
        _list = _ENCODING_LIST

    last_err = None
    for enc in _list:
        try:
            return data.decode(encoding=enc)
        except UnicodeDecodeError as err:
            last_err = err

    raise last_err


_T = TypeVar('_T')


def auto_encode_support(func: Callable[[Union[bytes, bytearray], ], _T]) \
        -> Callable[[Union[bytes, bytearray, str], ], _T]:
    def _func(data: Union[bytes, bytearray, str]) -> _T:
        if isinstance(data, (bytes, bytearray)):
            return func(data)
        elif isinstance(data, str):
            return func(auto_encode(data))
        else:
            raise TypeError("Unknown type to encode support - {cls}".format(cls=type(data).__class__))

    return _func


def auto_decode_support(func: Callable[..., Union[bytes, bytearray, str]]) -> Callable[..., str]:
    def _func(*args, **kwargs) -> str:
        result = func(*args, **kwargs)
        if isinstance(result, (bytes, bytearray)):
            return auto_decode(result)
        elif isinstance(result, str):
            return result
        else:
            raise TypeError("Unknown type to decode support - {cls}".format(cls=type(result).__class__))

    return _func
