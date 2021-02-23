from typing import List

from .base import FileOutputTemplate, FileOutput
from .general import load_output_template
from ....utils import get_repr_info


class _IFileOutputCollection:
    def __init__(self, outputs):
        """
        :param outputs: file outputs
        """
        self.__outputs = outputs

    def __repr__(self):
        """
        :return: representation string
        """
        return get_repr_info(
            cls=self.__class__,
            args=[
                ('outputs', lambda: len(self.__outputs)),
            ]
        )


class FileOutputCollectionTemplate(_IFileOutputCollection):
    def __init__(self, *outputs):
        """
        :param outputs: file output templates
        """
        self.__outputs = [load_output_template(item) for item in outputs]
        _IFileOutputCollection.__init__(self, self.__outputs)

    @property
    def outputs(self) -> List[FileOutputTemplate]:
        return list(self.__outputs)

    def __call__(self, **kwargs):
        """
        generate file output collection
        :param kwargs: plenty of arguments
        :return: file output collection
        """
        return FileOutputCollection(*[item(**kwargs) for item in self.__outputs])

    @classmethod
    def loads(cls, data) -> 'FileOutputCollectionTemplate':
        """
        load file output collection template from data
        :param data: raw data
        :return: file output collection template
        """
        if isinstance(data, cls):
            return data
        elif isinstance(data, (list, tuple)):
            return cls(*data)
        else:
            raise TypeError('Array or {type} expected but {actual} found.'.format(
                type=cls.__name__, actual=repr(type(data).__name__)))


class FileOutputCollection(_IFileOutputCollection):
    def __init__(self, *outputs):
        """
        :param outputs: file outputs
        """
        self.__outputs = list(outputs)
        _IFileOutputCollection.__init__(self, self.__outputs)

    @property
    def outputs(self) -> List[FileOutput]:
        return list(self.__outputs)

    def __call__(self):
        """
        execute this file output setting
        """
        for item in self.__outputs:
            item()
