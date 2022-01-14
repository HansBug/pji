import resource
import signal
import time

import pytest
from bitmath import MiB

from pji.control.model import ProcessResult

_DEMO_RUSAGE = resource.struct_rusage((2.0, 1.0, 131072, 0, 0, 0, 2216, 0, 0, 0, 0, 0, 0, 0, 246, 129))

_TIME_0_0 = time.time()
_TIME_1_0 = _TIME_0_0 + 1.0
_TIME_1_5 = _TIME_0_0 + 1.5
_TIME_3_0 = _TIME_0_0 + 3.0
_TIME_5_5 = _TIME_0_0 + 5.5


@pytest.mark.unittest
class TestControlModelProcessNormal:
    def test_properties(self):
        pr = ProcessResult(
            status=0,
            start_time=_TIME_0_0,
            end_time=_TIME_1_5,
            resource_usage=_DEMO_RUSAGE,
        )

        assert pr.exitcode == 0
        assert pr.signal_code == 0
        assert pr.signal is None
        assert pr.ok

        assert pr.start_time == _TIME_0_0
        assert pr.end_time == _TIME_1_5
        assert pr.real_time == 1.5

        assert pr.resource_usage == _DEMO_RUSAGE
        assert pr.cpu_time == 2.0
        assert pr.system_time == 1.0
        assert pr.max_memory == MiB(128).bytes

    def test_repr(self):
        pr = ProcessResult(
            status=0,
            start_time=_TIME_0_0,
            end_time=_TIME_5_5,
            resource_usage=_DEMO_RUSAGE,
        )

        assert repr(pr) == '<ProcessResult exitcode: 0, real time: 5.500s, cpu time: 2.000s, max memory: 128.0 MiB>'

    def test_json(self):
        pr = ProcessResult(
            status=0,
            start_time=_TIME_0_0,
            end_time=_TIME_1_5,
            resource_usage=_DEMO_RUSAGE,
        )

        assert pr.json == {
            'cpu_time': 2.0,
            'exitcode': 0,
            'max_memory': 134217728.0,
            'real_time': 1.5,
            'signal': None
        }


@pytest.mark.unittest
class TestControlModelProcessKilled:
    def test_properties(self):
        pr = ProcessResult(
            status=9,
            start_time=_TIME_0_0,
            end_time=_TIME_3_0,
            resource_usage=_DEMO_RUSAGE,
        )

        assert pr.exitcode == 0
        assert pr.signal_code == 9
        assert pr.signal == signal.SIGKILL
        assert not pr.ok

        assert pr.start_time == _TIME_0_0
        assert pr.end_time == _TIME_3_0
        assert pr.real_time == 3.0

        assert pr.resource_usage == _DEMO_RUSAGE
        assert pr.cpu_time == 2.0
        assert pr.system_time == 1.0
        assert pr.max_memory == MiB(128).bytes

    def test_repr(self):
        pr = ProcessResult(
            status=9,
            start_time=_TIME_0_0,
            end_time=_TIME_1_0,
            resource_usage=_DEMO_RUSAGE,
        )

        assert repr(pr) == '<ProcessResult exitcode: 0, signal: SIGKILL, real time: 1.000s, ' \
                           'cpu time: 2.000s, max memory: 128.0 MiB>'
