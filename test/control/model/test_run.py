import os

import pytest

from pji.control.model import ProcessResult, RunResult, ResourceLimit, RunResultStatus
from .test_process import _DEMO_RUSAGE, _TIME_1_5, _TIME_0_0

_DEMO_RESULT_NORMAL = ProcessResult(
    status=0,
    start_time=_TIME_0_0,
    end_time=_TIME_1_5,
    resource_usage=_DEMO_RUSAGE
)

_DEMO_RESULT_RUNTIME_ERROR = ProcessResult(
    status=256,
    start_time=_TIME_0_0,
    end_time=_TIME_1_5,
    resource_usage=_DEMO_RUSAGE
)

_DEMO_RESULT_KILLED = ProcessResult(
    status=9,
    start_time=_TIME_0_0,
    end_time=_TIME_1_5,
    resource_usage=_DEMO_RUSAGE
)


@pytest.mark.unittest
class TestControlModelRun:
    def test_normal_1(self):
        rr = RunResult(
            ResourceLimit(),
            _DEMO_RESULT_NORMAL,
        )

        assert rr.limit == ResourceLimit()
        assert rr.result is _DEMO_RESULT_NORMAL

        assert rr.ok
        assert rr.status == RunResultStatus.SUCCESS
        assert repr(rr) == '<RunResult status: SUCCESS>'

    def test_real_time_limit_exceed_1(self):
        rr = RunResult(
            ResourceLimit(max_real_time=1.0),
            _DEMO_RESULT_RUNTIME_ERROR,
        )

        assert rr.limit == ResourceLimit(max_real_time=1.0)
        assert rr.result is _DEMO_RESULT_RUNTIME_ERROR

        assert not rr.ok
        assert rr.status == RunResultStatus.REAL_TIME_LIMIT_EXCEED
        assert repr(rr) == '<RunResult status: REAL_TIME_LIMIT_EXCEED, exitcode: 1>'

    def test_real_time_limit_exceed_2(self):
        rr = RunResult(
            ResourceLimit(max_real_time=1.0),
            _DEMO_RESULT_KILLED,
        )

        assert rr.limit == ResourceLimit(max_real_time=1.0)
        assert rr.result is _DEMO_RESULT_KILLED

        assert not rr.ok
        assert rr.status == RunResultStatus.REAL_TIME_LIMIT_EXCEED
        assert repr(rr) == '<RunResult status: REAL_TIME_LIMIT_EXCEED, signal: SIGKILL>'

    def test_cpu_time_limit_exceed_1(self):
        rr = RunResult(
            ResourceLimit(max_cpu_time=1.0),
            _DEMO_RESULT_RUNTIME_ERROR,
        )

        assert rr.limit == ResourceLimit(max_cpu_time=1.0)
        assert rr.result is _DEMO_RESULT_RUNTIME_ERROR

        assert not rr.ok
        assert rr.status == RunResultStatus.CPU_TIME_LIMIT_EXCEED
        assert repr(rr) == '<RunResult status: CPU_TIME_LIMIT_EXCEED, exitcode: 1>'

    def test_cpu_time_limit_exceed_2(self):
        rr = RunResult(
            ResourceLimit(max_cpu_time=1.0),
            _DEMO_RESULT_KILLED,
        )

        assert rr.limit == ResourceLimit(max_cpu_time=1.0)
        assert rr.result is _DEMO_RESULT_KILLED

        assert not rr.ok
        assert rr.status == RunResultStatus.CPU_TIME_LIMIT_EXCEED
        assert repr(rr) == '<RunResult status: CPU_TIME_LIMIT_EXCEED, signal: SIGKILL>'

    def test_memory_limit_exceed_1(self):
        rr = RunResult(
            ResourceLimit(max_memory='64mb'),
            _DEMO_RESULT_KILLED,
        )

        assert rr.limit == ResourceLimit(max_memory='64 mb')
        assert rr.result is _DEMO_RESULT_KILLED

        assert not rr.ok
        assert rr.status == RunResultStatus.MEMORY_LIMIT_EXCEED
        assert repr(rr) == '<RunResult status: MEMORY_LIMIT_EXCEED, signal: SIGKILL>'

    def test_memory_limit_exceed_2(self):
        rr = RunResult(
            ResourceLimit(max_memory='64mb'),
            _DEMO_RESULT_RUNTIME_ERROR,
        )

        assert rr.limit == ResourceLimit(max_memory='64 mb')
        assert rr.result is _DEMO_RESULT_RUNTIME_ERROR

        assert not rr.ok
        assert rr.status == RunResultStatus.MEMORY_LIMIT_EXCEED
        assert repr(rr) == '<RunResult status: MEMORY_LIMIT_EXCEED, exitcode: 1>'

    def test_runtime_error(self):
        rr = RunResult(
            ResourceLimit(),
            _DEMO_RESULT_RUNTIME_ERROR,
        )

        assert rr.limit == ResourceLimit()
        assert rr.result is _DEMO_RESULT_RUNTIME_ERROR

        assert not rr.ok
        assert rr.status == RunResultStatus.RUNTIME_ERROR
        assert repr(rr) == '<RunResult status: RUNTIME_ERROR, exitcode: 1>'

    def test_system_error(self):
        rr = RunResult(
            ResourceLimit(),
            _DEMO_RESULT_KILLED,
        )

        assert rr.limit == ResourceLimit()
        assert rr.result is _DEMO_RESULT_KILLED

        assert not rr.ok
        assert rr.status == RunResultStatus.SYSTEM_ERROR
        assert repr(rr) == '<RunResult status: SYSTEM_ERROR, signal: SIGKILL>'


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
