from typing import List, Tuple, Optional, Union

from ...utils import auto_encode_support

_auto_encode = auto_encode_support(lambda x: x)

_LINE_TYPING = Union[bytes, bytearray, str]
_TIMING_LINE_TYPING = Tuple[float, _LINE_TYPING]
_TIMING_LIST_TYPING = List[_TIMING_LINE_TYPING]


def _stable_process(lines: _TIMING_LIST_TYPING) -> _TIMING_LIST_TYPING:
    lines = [(float(_time), _auto_encode(_line)) for _time, _line in lines]
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
