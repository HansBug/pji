import resource

from bitmath import MiB

from ...utils import allow_none, size_to_bytes, time_to_duration

_memory_process = allow_none(size_to_bytes)
_duration_process = allow_none(time_to_duration)
_number_process = allow_none(lambda x: x)


class ResourceLimit:
    __RESOURCE_UNLIMITED = -1
    __RESOURCE_LIMITS = {"max_stack", "max_memory", "max_cpu_time", "max_real_time",
                         "max_process_number", "max_output_size", }

    def __init__(
            self,
            max_stack=None,
            max_memory=None,
            max_cpu_time=None,
            max_real_time=None,
            max_process_number=None,
            max_output_size=None
    ):
        """
        :param max_stack: max stack memory (unit: B)
        :param max_memory: max rss memory memory (unit: B)
        :param max_cpu_time: max cpu time (unit: s)
        :param max_real_time: max real time (unit: s)
        :param max_process_number: max process count
        :param max_output_size: max output size (unit: B)
        """
        self.__max_stack = _memory_process(max_stack)
        self.__max_memory = _memory_process(max_memory)
        self.__max_cpu_time = _duration_process(max_cpu_time)
        self.__max_real_time = _duration_process(max_real_time)
        self.__max_process_number = _number_process(max_process_number)
        self.__max_output_size = _memory_process(max_output_size)

    @property
    def max_stack(self):
        """
        :return: max stack size (size: B)
        """
        return self.__max_stack

    @property
    def max_memory(self):
        """
        :return: max rss memory size (size: B)
        """
        return self.__max_memory

    @property
    def max_cpu_time(self):
        """
        :return: max cpu time (unit: s)
        """
        return self.__max_cpu_time

    @property
    def max_real_time(self):
        """
        :return: max real time (unit: s)
        """
        return self.__max_real_time

    @property
    def max_process_number(self):
        """
        :return: max process count
        """
        return self.__max_process_number

    @property
    def max_output_size(self):
        """
        :return: max output size (unit: B)
        """
        return self.__max_output_size

    @classmethod
    def __apply_limit(cls, limit_type, value):
        """
        apply one of the resources
        :param limit_type: type of limitation
        :param value: limitation value
        """
        resource.setrlimit(limit_type, (value, value))

    def __apply_max_stack(self):
        """
        apply max stack limit
        """
        if self.max_stack:
            real = self.max_stack
        else:
            real = self.__RESOURCE_UNLIMITED
        self.__apply_limit(resource.RLIMIT_STACK, real)

    def __apply_max_memory(self):
        """
        apply max rss memory limit
        """
        if self.max_memory:
            real = round(self.max_memory + MiB(256).bytes)
        else:
            real = self.__RESOURCE_UNLIMITED
        self.__apply_limit(resource.RLIMIT_AS, real)

    def __apply_max_cpu_time(self):
        """
        apply max cpu time limit
        """
        if self.max_cpu_time:
            real = round(self.max_cpu_time) + 1
        else:
            real = self.__RESOURCE_UNLIMITED
        self.__apply_limit(resource.RLIMIT_CPU, real)

    def __apply_max_process_number(self):
        """
        apply max process number limit
        """
        if self.max_process_number:
            real = self.max_process_number
        else:
            real = self.__RESOURCE_UNLIMITED
        self.__apply_limit(resource.RLIMIT_NPROC, real)

    def __apply_max_output_size(self):
        """
        apply max output size limit
        """
        if self.max_output_size:
            real = self.max_output_size
        else:
            real = self.__RESOURCE_UNLIMITED
        self.__apply_limit(resource.RLIMIT_FSIZE, real)

    @property
    def json(self):
        """
        get json format data
        :return: json format data
        """
        return {
            "max_memory": self.max_memory,
            "max_stack": self.max_stack,
            "max_process_number": self.max_process_number,
            "max_output_size": self.max_output_size,
            "max_cpu_time": self.max_cpu_time,
            "max_real_time": self.max_real_time,
        }

    @classmethod
    def load_from_json(cls, json_data: dict) -> 'ResourceLimit':
        """
        load object from json data
        :param json_data: json data
        :return: resource limit object
        """
        return cls(**cls.__filter_by_properties(**json_data))

    def apply(self):
        """
        apply the resource limits
        """
        self.__apply_max_process_number()
        self.__apply_max_stack()
        self.__apply_max_memory()
        self.__apply_max_output_size()
        self.__apply_max_cpu_time()

    @classmethod
    def __filter_by_properties(cls, **kwargs):
        """
        filter the arguments by properties
        :param kwargs: original arguments
        :return: filtered arguments
        """
        return {
            key: value for key, value in kwargs.items() if key in cls.__RESOURCE_LIMITS
        }

    @classmethod
    def merge(cls, *limits: 'ResourceLimit'):
        """
        merge some of the limits
        :param limits: list of the limits
        :return: merged limits
        """

        def _get_min_limitation(array, property_method):
            _values = [_item for _item in [property_method(_item) for _item in array if _item] if _item is not None]
            if _values:
                return min(_values)
            else:
                return None

        _max_stack = _get_min_limitation(limits, lambda _item: _item.max_stack)
        _max_memory = _get_min_limitation(limits, lambda _item: _item.max_memory)
        _max_cpu_time = _get_min_limitation(limits, lambda _item: _item.max_cpu_time)
        _max_real_time = _get_min_limitation(limits, lambda _item: _item.max_real_time)
        _max_process_number = _get_min_limitation(limits, lambda _item: _item.max_process_number)
        _max_output_size = _get_min_limitation(limits, lambda _item: _item.max_output_size)

        return cls(
            max_stack=_max_stack,
            max_memory=_max_memory,
            max_cpu_time=_max_cpu_time,
            max_real_time=_max_real_time,
            max_process_number=_max_process_number,
            max_output_size=_max_output_size,
        )
