import os
from functools import wraps
from typing import Optional

from ..model import ResourceLimit, Identification


def _do_nothing():
    pass


def _attach_preexec_fn(preexec_fn=None, pre_attach=None, post_attach=None):
    preexec_fn = preexec_fn or _do_nothing
    pre_attach = pre_attach or _do_nothing
    post_attach = post_attach or _do_nothing

    @wraps(preexec_fn)
    def _new_preexec_fn():
        pre_attach()
        preexec_fn()
        post_attach()

    return _new_preexec_fn


def workdir_setter(func):
    @wraps(func)
    def _func(*args, cwd: Optional[str] = None, preexec_fn=None, **kwargs):
        cwd = cwd or os.getcwd()
        if not os.path.exists(cwd):
            raise FileNotFoundError('Path {cwd} not found.'.format(cwd=repr(cwd)))
        if not os.path.isdir(cwd):
            raise NotADirectoryError('{cwd} is not a directory.'.format(cwd=repr(cwd)))

        def _change_dir_func():
            os.chdir(cwd)

        preexec_fn = _attach_preexec_fn(preexec_fn, pre_attach=_change_dir_func)
        return func(*args, preexec_fn=preexec_fn, **kwargs)

    return _func


_REAL_TIME_LIMIT_KEY = 'real_time_limit'


def resources_setter(func):
    @wraps(func)
    def _func(*args, resources=None, preexec_fn=None, **kwargs):
        resources = ResourceLimit.loads(resources)

        def _apply_resource_limit_func():
            resources.apply()

        preexec_fn = _attach_preexec_fn(preexec_fn, post_attach=_apply_resource_limit_func)
        return func(*args, preexec_fn=preexec_fn, resources=resources, **kwargs)

    return _func


def users_setter(func):
    @wraps(func)
    def _func(*args, user=None, group=None, preexec_fn=None, **kwargs):
        identification = Identification(user, group, auto_group=True)

        def _apply_user_func():
            identification.apply()

        preexec_fn = _attach_preexec_fn(preexec_fn, post_attach=_apply_user_func)
        return func(*args, preexec_fn=preexec_fn, **kwargs)

    return _func


def process_setter(func):
    @wraps(func)
    @users_setter
    @resources_setter
    @workdir_setter
    def _func(*args, **kwargs):
        return func(*args, **kwargs)

    return _func
