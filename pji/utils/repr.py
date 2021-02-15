from typing import List, Tuple, Union, Callable


def get_repr_info(cls: type, args: List[Tuple[str, Union[Callable, Tuple[Callable, Callable]]]]):
    _data_items = []
    for name, fd in args:
        if isinstance(fd, tuple):
            _data_func, _present_func = fd
        else:
            _data_func, _present_func = fd, lambda: True

        if _present_func():
            _data_items.append('{name}: {data}'.format(name=name, data=_data_func()))

    if _data_items:
        return '<{cls} {data}>'.format(cls=cls.__name__, data=', '.join(_data_items))
    else:
        return '<{cls}>'.format(cls=cls.__name__)
