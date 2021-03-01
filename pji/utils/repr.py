from typing import List, Tuple


def get_repr_info(cls: type, args: List[Tuple]):
    """
    get representation information
    :param cls: class object
    :param args: arguments to display
    :return: representation string
    """
    _data_items = []
    for item in args:
        if isinstance(item, tuple):
            if len(item) == 2:
                name, fd = item
                if isinstance(fd, tuple):
                    _data_func, _present_func = fd
                else:
                    _data_func, _present_func = fd, lambda: True
            elif len(item) == 3:
                name, _data_func, _present_func = item
            else:
                raise ValueError('Tuple\'s length should be 2 or 3 but {actual} found.'.format(actual=repr(len(item))))

            if _present_func():
                _data_items.append('{name}: {data}'.format(name=name, data=_data_func()))
        else:
            raise TypeError(
                'Argument item should be tuple but {actual} found.'.format(actual=repr(type(item).__name__)))

    if _data_items:
        return '<{cls} {data}>'.format(cls=cls.__name__, data=', '.join(_data_items))
    else:
        return '<{cls}>'.format(cls=cls.__name__)
