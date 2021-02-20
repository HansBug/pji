import os


def is_absolute_path(path: str) -> bool:
    return os.path.isabs(path)


def is_relative_path(path: str) -> bool:
    return not os.path.isabs(path)


def is_inner_relative_path(path: str) -> bool:
    if is_relative_path(path):
        return os.path.normpath(path).split(os.sep)[0] != '..'
    else:
        return False
