import os
import signal
from typing import Optional

import bitmath


class _IStatus:
    def __init__(self, status: int):
        self.__status = status

    @property
    def exitcode(self) -> int:
        """
        :return: exitcode of process
        """
        return os.WEXITSTATUS(self.__status)

    @property
    def signal_code(self) -> int:
        """
        :return: signal code of process
        """
        return os.WTERMSIG(self.__status)

    @property
    def signal(self) -> Optional[signal.Signals]:
        """
        :return: signal object
        """
        if self.signal_code:
            return signal.Signals(self.signal_code)
        else:
            return None

    @property
    def ok(self) -> bool:
        """
        :return: true if quit normally, otherwise false
        """
        return not self.__status


class _IDuration:
    def __init__(self, start_time: float, end_time: float):
        """
        :param start_time: process start time
        :param end_time: process end time
        """
        self.__start_time = start_time
        self.__end_time = end_time

    @property
    def start_time(self):
        """
        :return: start time of process
        """
        return self.__start_time

    @property
    def end_time(self):
        """
        :return: end time of process
        """
        return self.__end_time

    @property
    def real_time(self):
        """
        :return: duration of process
        """
        if self.start_time is not None and self.end_time is not None:
            return self.end_time - self.start_time
        else:
            return None


class _IResource:
    def __init__(self, resource_usage):
        self.__resource_usage = resource_usage

    @property
    def resource_usage(self):
        """
        获取资源占用对象
        :return: 资源占用对象
        """
        return self.__resource_usage

    @property
    def cpu_time(self):
        """
        获取cpu时间使用（单位：秒）
        :return: cpu时间使用（单位：秒）
        """
        return self.__resource_usage.ru_utime

    @property
    def system_time(self):
        """
        获取系统时间使用（单位：秒）
        :return: 系统时间使用（单位：秒）
        """
        return self.__resource_usage.ru_stime

    @property
    def max_memory(self):
        """
        获取最大内存占用（单位：字节）
        :return: 最大内存占用（单位：字节）
        """
        return self.__resource_usage.ru_maxrss * 1024.0


class ProcessResult(_IStatus, _IDuration, _IResource):
    def __init__(self, status, start_time, end_time, resource_usage):
        """
        :param status: result status
        :param start_time: start time of process
        :param end_time: end time of process
        :param resource_usage: resource usage
        """
        _IStatus.__init__(self, status)
        _IDuration.__init__(self, start_time, end_time)
        _IResource.__init__(self, resource_usage)

    def __repr__(self):
        """
        :return: get presentation format
        """
        return "<{cls} exitcode: {exitcode}, signal: {signal}, real time: {real_time}, " \
               "cpu time: {cpu_time}, max memory: {max_memory}>".format(cls=type(self).__name__,
                                                                        exitcode=self.exitcode,
                                                                        signal=self.signal_code,
                                                                        real_time='%.3fs' % self.real_time,
                                                                        cpu_time='%.3fs' % self.cpu_time,
                                                                        max_memory=bitmath.Byte(
                                                                            self.max_memory).best_prefix(), )
