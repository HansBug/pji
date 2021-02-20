import os


def is_absolute_path(path: str) -> bool:
    return os.path.isabs(path)


def is_relative_path(path: str) -> bool:
    return not os.path.isabs(path)


def is_inner_relative_path(path: str, allow_root: bool = True) -> bool:
    if is_relative_path(path):
        segments = os.path.normpath(path).split(os.sep)
        if not allow_root and segments == ['.']:
            return False
        else:
            return segments[0] != '..'
    else:
        return False
