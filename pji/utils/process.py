import os
import signal


# noinspection PyBroadException
def kill_by_pid(pid, safe=True):
    """
    kill process by thread
    :param pid: process id
    :param safe: whether use safe mode (in safe mode, no exception will be raised)
    :return: success or not
    """

    def _kill_process():
        return os.kill(pid, signal.SIGKILL)

    if not safe:
        _kill_process()
        return True
    else:
        try:
            _kill_process()
            return True
        except Exception:
            return False
