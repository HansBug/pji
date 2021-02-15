from enum import unique, IntEnum
from typing import Optional

from .process import ProcessResult
from .resource import ResourceLimit
from ...utils import get_repr_info


@unique
class RunResultStatus(IntEnum):
    NOT_COMPLETED = -1
    ACCEPTED = 0
    CPU_TIME_LIMIT_EXCEED = 1
    REAL_TIME_LIMIT_EXCEED = 2
    MEMORY_LIMIT_EXCEED = 3
    RUNTIME_ERROR = 4
    SYSTEM_ERROR = 5

    @property
    def ok(self):
        return self == RunResultStatus.ACCEPTED

    @property
    def completed(self):
        return self != RunResultStatus.NOT_COMPLETED


class RunResult:
    def __init__(self, limit: ResourceLimit, result: Optional[ProcessResult]):
        self.__limit = limit
        self.__result = result

    @property
    def limit(self) -> ResourceLimit:
        return self.__limit

    @property
    def result(self) -> ProcessResult:
        return self.__result

    @property
    def status(self) -> RunResultStatus:
        if self.__result is None:
            return RunResultStatus.NOT_COMPLETED
        elif self.__limit.max_cpu_time is not None and self.__result.cpu_time > self.__limit.max_cpu_time:
            return RunResultStatus.CPU_TIME_LIMIT_EXCEED
        elif self.__limit.max_real_time is not None and self.__result.real_time > self.__limit.max_real_time:
            return RunResultStatus.REAL_TIME_LIMIT_EXCEED
        elif self.__limit.max_memory is not None and self.__result.max_memory > self.__limit.max_memory:
            return RunResultStatus.MEMORY_LIMIT_EXCEED
        elif self.__result.exitcode != 0:
            return RunResultStatus.RUNTIME_ERROR
        elif not self.__result.ok:
            return RunResultStatus.SYSTEM_ERROR
        else:
            return RunResultStatus.ACCEPTED

    @property
    def ok(self) -> bool:
        return self.__result.ok and self.status.ok

    @property
    def completed(self) -> bool:
        return self.status.completed

    def __repr__(self):
        return get_repr_info(
            cls=self.__class__,
            args=[
                ('status', lambda: self.status.name),
                ('exitcode', (lambda: self.result.exitcode, lambda: self.result.exitcode != 0)),
                ('signal', (lambda: self.result.signal.name, lambda: self.result.signal is not None)),
            ],
        )
