import os
import shutil


def _auto_delete(filename: str):
    if os.path.isdir(filename):
        shutil.rmtree(filename, ignore_errors=True)
    else:
        os.remove(filename)


def _auto_copy(from_file: str, to_file: str):
    if not os.path.exists(from_file):
        raise FileNotFoundError('File {filename} not found.'.format(filename=repr(from_file)))
    if not os.access(from_file, os.R_OK):
        raise PermissionError('File {filename} unreadable.'.format(filename=repr(from_file)))

    if os.path.exists(to_file):
        _auto_delete(to_file)
    if os.path.isdir(from_file):
        shutil.copytree(from_file, to_file)
    else:
        shutil.copyfile(from_file, to_file, follow_symlinks=True)
