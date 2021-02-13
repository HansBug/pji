import time
from threading import Thread
from typing import List, Tuple

from pji.control.process import InteractiveProcess


def time_based_interaction(interactive: InteractiveProcess, _time_scripts: List[Tuple[float, str]],
                           hard: bool = False, hook=None):
    _output_lines = []

    def _output_loop():
        nonlocal _output_lines
        for _rel_time, _tag, _line in interactive.output_yield:
            _output_lines.append((_rel_time, _tag, _line))
            if hook is not None:
                hook(_rel_time, _tag, _line)

    output_loop_thread = Thread(target=_output_loop)
    output_loop_thread.start()

    _time_scripts = [(_time, _line) for _time, _index, _line in sorted(
        [(_rel_time, _index, _line) for _index, (_rel_time, _line) in enumerate(_time_scripts)])]

    if hard:
        def _input_loop():
            for _rel_time, _line in _time_scripts:
                time.sleep(max(interactive.start_time + _rel_time - time.time(), 0))
                yield _rel_time, _line
    else:
        def _input_loop():
            _delta_scripts = [(_time, _time - (_time_scripts[_index - 1][0] if _index > 0 else 0), _line) for
                              _index, (_time, _line) in enumerate(_time_scripts)]
            for _rel_time, _delta, _line in _delta_scripts:
                time.sleep(_delta)
                yield _rel_time, _line

    with interactive as it:
        for rel_time, line in _input_loop():
            it.print_stdin(bytes(line, 'utf8'))

    output_loop_thread.join()
    return _output_lines
