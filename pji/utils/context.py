from contextlib import contextmanager


@contextmanager
def eclosing(obj, close: bool = True):
    try:
        yield obj
    finally:
        if close:
            obj.close()
