import pytest

from pji.utils import eclosing


class _Closer:
    def __init__(self, close_hook):
        self.__close_hook = close_hook

    def close(self):
        self.__close_hook()


@pytest.mark.unittest
class TestUtilsContext:
    def test_eclosing(self):
        _closed = False

        def _close_func():
            nonlocal _closed
            _closed = True

        c = _Closer(_close_func)
        with eclosing(c) as _c:
            assert c is _c

        assert _closed

    def test_eclosing_not_close(self):
        _closed = False

        def _close_func():
            nonlocal _closed
            _closed = True

        c = _Closer(_close_func)
        with eclosing(c, False) as _c:
            assert c is _c

        assert not _closed

    # noinspection PyBroadException
    def test_eclosing_exception(self):
        _closed = False

        def _close_func():
            nonlocal _closed
            _closed = True

        c = _Closer(_close_func)
        try:
            with eclosing(c) as _c:
                raise RuntimeError
        except RuntimeError:
            assert _closed
        except Exception:
            pytest.fail('Should not reach here.')
        else:
            pytest.fail('Should not reach here.')
