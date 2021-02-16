from typing import Union

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
