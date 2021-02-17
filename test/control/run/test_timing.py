import io
import os

import pytest

from pji.control.run import TimingScript
from pji.utils import JsonLoadError


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestControlRunTimingScript:
    def test_load_ident(self):
        _text = """
[0.0]this is first line
 [2.5]this is third line
 [ 1.0]this is second line

# this is comment
 [ 3.0 ]this is last line
        """

        with io.StringIO(_text) as f:
            _ts = TimingScript.load(f)

        assert isinstance(_ts, TimingScript)
        assert _ts.lines == [
            (0.0, b'this is first line'),
            (1.0, b'this is second line'),
            (2.5, b'this is third line'),
            (3.0, b'this is last line'),
        ]
        assert _ts.delta_lines == [
            (0.0, b'this is first line'),
            (1.0, b'this is second line'),
            (1.5, b'this is third line'),
            (0.5, b'this is last line'),
        ]

    def test_load_yaml(self):
        _text = """
- time: 0
  line: this is first line
- time: 3.0
  lines: this is last line
- time: 2.5
  line:
    - this is third line
- time: 1
  lines:
    - this is second line
                """

        with io.StringIO(_text) as f:
            _ts = TimingScript.load(f)

        assert isinstance(_ts, TimingScript)
        assert _ts.lines == [
            (0.0, b'this is first line'),
            (1.0, b'this is second line'),
            (2.5, b'this is third line'),
            (3.0, b'this is last line'),
        ]
        assert _ts.delta_lines == [
            (0.0, b'this is first line'),
            (1.0, b'this is second line'),
            (1.5, b'this is third line'),
            (0.5, b'this is last line'),
        ]

    def test_load_json(self):
        _text = """
[
    {"time": 0, line: "this is first line"},
    {"time": 3.0, lines: "this is last line"},
    {"time": 2.5, line: ["this is third line"]},
    {"time": 1, lines: ["this is second line"]}
]
                """

        with io.StringIO(_text) as f:
            _ts = TimingScript.load(f)

        assert isinstance(_ts, TimingScript)
        assert _ts.lines == [
            (0.0, b'this is first line'),
            (1.0, b'this is second line'),
            (2.5, b'this is third line'),
            (3.0, b'this is last line'),
        ]
        assert _ts.delta_lines == [
            (0.0, b'this is first line'),
            (1.0, b'this is second line'),
            (1.5, b'this is third line'),
            (0.5, b'this is last line'),
        ]

    def test_load_invalid_1(self):
        _text = """
        [1s3]fk
        """

        with pytest.raises(JsonLoadError):
            with io.StringIO(_text) as f:
                TimingScript.load(f)

    def test_load_invalid_2(self):
        _text = """
        lksdgflksdfl;g
        """

        with pytest.raises(TypeError):
            with io.StringIO(_text) as f:
                TimingScript.load(f)

    def test_load_invalid_3(self):
        _text = """
        [
            {"time": 0, line: "this is first line"},
            "klsdfgjlk",
            {"time": 2.5, line: ["this is third line"]},
            {"time": 1, lines: ["this is second line"]}
        ]
                        """
        with pytest.raises(TypeError):
            with io.StringIO(_text) as f:
                TimingScript.load(f)

    def test_load_invalid_4(self):
        _text = """
        [
            {"time": 0, line: {"name": "this is first line"}},
            {"time": 2.5, line: ["this is third line"]},
            {"time": 1, lines: ["this is second line"]}
        ]
                        """
        with pytest.raises(TypeError):
            with io.StringIO(_text) as f:
                TimingScript.load(f)

    def test_load_invalid_5(self):
        _text = """
        [
            {"time": 0, line: "this is first line"},
            {"time": 3.0, lines: "this is last line"},
            {"timex": 2.5, line: ["this is third line"]},
            {"time": 1, lines: ["this is second line"]}
        ]
                        """

        with pytest.raises(KeyError):
            with io.StringIO(_text) as f:
                TimingScript.load(f)

    def test_loads_str_1(self):
        _ts = TimingScript.loads(TimingScript([
            (0.0, b'this is first line'),
            (1.0, b'this is second line'),
            (2.5, b'this is third line'),
            (3.0, b'this is last line'),
        ]))

        assert isinstance(_ts, TimingScript)
        assert _ts.lines == [
            (0.0, b'this is first line'),
            (1.0, b'this is second line'),
            (2.5, b'this is third line'),
            (3.0, b'this is last line'),
        ]
        assert _ts.delta_lines == [
            (0.0, b'this is first line'),
            (1.0, b'this is second line'),
            (1.5, b'this is third line'),
            (0.5, b'this is last line'),
        ]

    def test_loads_str_2(self):
        _ts = TimingScript.loads([
            (0.0, b'this is first line'),
            (1.0, b'this is second line'),
            (2.5, b'this is third line'),
            (3.0, b'this is last line'),
        ])

        assert isinstance(_ts, TimingScript)
        assert _ts.lines == [
            (0.0, b'this is first line'),
            (1.0, b'this is second line'),
            (2.5, b'this is third line'),
            (3.0, b'this is last line'),
        ]
        assert _ts.delta_lines == [
            (0.0, b'this is first line'),
            (1.0, b'this is second line'),
            (1.5, b'this is third line'),
            (0.5, b'this is last line'),
        ]

    def test_loads_str_3(self):
        _ts = TimingScript.loads("""
        [0.0]this is first line
 [2.5]this is third line
 [ 1.0]this is second line

# this is comment
 [ 3.0 ]this is last line
        """)

        assert isinstance(_ts, TimingScript)
        assert _ts.lines == [
            (0.0, b'this is first line'),
            (1.0, b'this is second line'),
            (2.5, b'this is third line'),
            (3.0, b'this is last line'),
        ]
        assert _ts.delta_lines == [
            (0.0, b'this is first line'),
            (1.0, b'this is second line'),
            (1.5, b'this is third line'),
            (0.5, b'this is last line'),
        ]

    def test_loads_str_4(self):
        _ts = TimingScript.loads(b"""
            [0.0]this is first line
     [2.5]this is third line
     [ 1.0]this is second line

    # this is comment
     [ 3.0 ]this is last line
            """)

        assert isinstance(_ts, TimingScript)
        assert _ts.lines == [
            (0.0, b'this is first line'),
            (1.0, b'this is second line'),
            (2.5, b'this is third line'),
            (3.0, b'this is last line'),
        ]
        assert _ts.delta_lines == [
            (0.0, b'this is first line'),
            (1.0, b'this is second line'),
            (1.5, b'this is third line'),
            (0.5, b'this is last line'),
        ]

    def test_loads_str_invalid(self):
        with pytest.raises(TypeError):
            TimingScript.loads(1)

    def test_eq(self):
        _ts = TimingScript([
            (0.0, b'this is first line'),
            (1.0, b'this is second line'),
            (2.5, b'this is third line'),
            (3.0, b'this is last line'),
        ])

        assert _ts == _ts
        assert _ts == TimingScript([
            (0.0, b'this is first line'),
            (1.0, b'this is second line'),
            (2.5, b'this is third line'),
            (3.0, b'this is last line'),
        ])
        assert not (_ts == 1)

    def test_repr(self):
        assert repr(TimingScript([
            (0.0, b'this is first line'),
            (1.0, b'this is second line'),
            (2.5, b'this is third line'),
            (3.0, b'this is last line'),
        ])) == '<TimingScript lines: 4, start_time: 0.000s, end_time: 3.000s>'
        assert repr(TimingScript()) == '<TimingScript lines: 0>'


@pytest.mark.unittest
class TestControlRunTimingRun:
    def test_timing_run(self):
        pass


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
