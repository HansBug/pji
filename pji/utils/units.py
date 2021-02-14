from bitmath import Byte
from bitmath import parse_string_unsafe as parse_bytes
from pytimeparse import parse as parse_duration


def size_to_bytes(size) -> int:
    if isinstance(size, int):
        return size
    elif isinstance(size, str):
        return parse_bytes(size).bytes
    elif isinstance(size, Byte):
        return size.bytes
    else:
        raise TypeError('{int}, {str} or {byte} expected but {actual} found.'.format(
            int=int.__name__,
            str=str.__name__,
            byte=Byte.__name__,
            actual=type(size).__name__,
        ))


def time_to_duration(time_):
    if isinstance(time_, (float, int)):
        return time_
    elif isinstance(time_, str):
        return parse_duration(time_)
    else:
        raise TypeError('{float}, {int} or {str} expected but {actual} found.'.format(
            float=float.__name__,
            int=int.__name__,
            str=str.__name__,
            actual=type(time_).__name__,
        ))
