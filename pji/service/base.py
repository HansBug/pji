import os

from ..utils import is_inner_relative_path, FilePool


def _check_os_path(path: str) -> str:
    """
    check file valid or not, when valid, just process it
    :param path: original file path
    :return: normalized file path
    """
    return os.path.normpath(path)


def _check_workdir_position(path: str) -> str:
    """
    check local path valid or not, when valid, just process it
    :param path: original local path
    :return: normalized local path
    """
    if not is_inner_relative_path(path):
        raise ValueError(
            'Inner relative position expected for local but {actual} found.'.format(actual=repr(path)))
    return os.path.normpath(path)


def _check_workdir_file(path: str) -> str:
    """
    check local path valid or not, when valid, just process it
    :param path: original local path
    :return: normalized local path
    """
    if not is_inner_relative_path(path, allow_root=False):
        raise ValueError(
            'Inner relative file path expected for local but {actual} found.'.format(actual=repr(path)))
    return os.path.normpath(path)


def _check_pool_tag(tag: str) -> str:
    """
    check if tag is valid, if valid, just return it
    :param tag: tag
    :return: original tag
    """
    FilePool.check_tag_name(tag)
    return tag
