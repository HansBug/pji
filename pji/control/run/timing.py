import re
from typing import List, Tuple, Optional, Union

from ...utils import auto_encode_support, auto_decode_support, auto_load_json, JsonLoadError, get_repr_info

_auto_encode = auto_encode_support(lambda x: x)
_auto_decode = auto_decode_support(lambda x: x)

_LINE_TYPING = Union[bytes, bytearray, str]
_TIMING_LINE_TYPING = Tuple[float, _LINE_TYPING]
_TIMING_LIST_TYPING = List[_TIMING_LINE_TYPING]


def _stable_process(lines: _TIMING_LIST_TYPING) -> _TIMING_LIST_TYPING:
    lines = [(float(_time), _auto_encode(_line).rstrip(b'\r\n')) for _time, _line in lines]
    _sorted = sorted([(_time, i, _line) for i, (_time, _line) in enumerate(lines)])
    return [(_time, _line) for _time, i, _line in _sorted]


def _to_delta_lines(lines: _TIMING_LIST_TYPING) -> _TIMING_LIST_TYPING:
    return [(_time - (lines[i - 1][0] if i > 0 else 0.0), _line) for i, (_time, _line) in enumerate(lines)]


class TimingScript:
    def __init__(self, lines: Optional[_TIMING_LIST_TYPING] = None):
        self.__lines = _stable_process(lines or [])

    @property
    def lines(self):
        return list(self.__lines)

    @property
    def delta_lines(self):
        return _to_delta_lines(self.__lines)

    @classmethod
    def load(cls, stream) -> 'TimingScript':
        return _load_from_stream(stream)

    def __eq__(self, other):
        if other is self:
            return True
        elif isinstance(other, TimingScript):
            return self.__lines == other.__lines
        else:
            return False

    def __repr__(self):
        return get_repr_info(
            cls=self.__class__,
            args=[
                ('lines', lambda: len(self.__lines)),
                ('start_time', (lambda: '%.3fs' % self.__lines[0][0], lambda: len(self.__lines) > 0)),
                ('end_time', (lambda: '%.3fs' % self.__lines[-1][0], lambda: len(self.__lines) > 0)),
            ]
        )


_LINE_IDENT = (re.compile(r'\s*\[\s*(\d+(\.\d*)?)\s*]([\s\S]*)'), (1, 3))
_LINE_COMMENT = re.compile(r'\s*#\s*[\s\S]*')


def _load_from_line_ident(stream) -> TimingScript:
    _result = []
    for line in stream:
        _str_line = _auto_decode(line).rstrip('\r\n')
        if _str_line.strip() and not _LINE_COMMENT.fullmatch(_str_line):
            _pattern, (_gtime, _gline) = _LINE_IDENT
            _match = _pattern.fullmatch(_str_line)
            if _match:
                _time, _line = float(_match[_gtime]), _auto_encode(_match[_gline])
                _result.append((_time, _line))
            else:
                raise ValueError('Invalid line {line} for timing script.'.format(line=repr(_str_line)))

    return TimingScript(_result)


def _load_from_json(stream) -> TimingScript:
    _json = auto_load_json(stream)
    if not isinstance(_json, list):
        raise TypeError('Timing script json should be a list but {actual} found.'.format(actual=type(_json).__name__))

    _result = []
    for _item in _json:
        if not isinstance(_item, dict):
            raise TypeError('Timing line should be a dict but {actual} found.'.format(actual=type(_item).__name__))

        _time = _item['time']
        try:
            _lines = _item['line']
        except KeyError:
            _lines = _item['lines']

        if isinstance(_lines, list):
            _lines = list(_lines)
        elif isinstance(_lines, dict):
            raise TypeError('Line should not be a dict.')
        else:
            _lines = [str(_lines)]

        for _line in _lines:
            _result.append((_time, _auto_encode(_line)))

    return TimingScript(_result)


_METHODS = [
    (_load_from_line_ident, ValueError),
    (_load_from_json, (JsonLoadError, TypeError, KeyError))
]


def _load_from_stream(stream) -> TimingScript:
    _init_position = stream.tell()
    _last_err = None

    for _func, _except in _METHODS:
        try:
            stream.seek(_init_position)
            return _func(stream)
        except _except as err:
            _last_err = err

    raise _last_err
