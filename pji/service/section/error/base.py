from abc import ABCMeta, abstractmethod


class ErrorInfoTemplate(metaclass=ABCMeta):
    @abstractmethod
    def __call__(self, *args, **kwargs) -> 'ErrorInfo':
        raise NotImplementedError


class ErrorInfo(metaclass=ABCMeta):
    @abstractmethod
    def __call__(self):
        raise NotImplementedError
