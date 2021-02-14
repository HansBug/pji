from bitmath import Byte
from bitmath import parse_string_unsafe as parse_bits


def size_to_bytes(size) -> int:
    if isinstance(size, int):
        return size
    elif isinstance(size, str):
        return parse_bits(size).bytes
    elif isinstance(size, Byte):
        return size.bytes
    else:
        raise TypeError('{int}, {str} or {byte} expected but {actual} found.'.format(
            int=int.__name__,
            str=str.__name__,
            byte=Byte.__name__,
            actual=type(size).__name__,
        ))
