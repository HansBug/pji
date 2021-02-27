import os
from threading import Thread

import pytest

from pji.utils import gen_lock


@pytest.mark.unittest
class TestUtilsIter:
    def test_gen_lock_simple(self):
        assert list(gen_lock([1, 2, 3, 4])) == [1, 2, 3, 4]

    def test_gen_lock_func(self):
        def _yield_func():
            for i in range(1, 5):
                yield i

        assert list(gen_lock(_yield_func())) == [1, 2, 3, 4]

    def test_gen_lock_threading(self):
        _original = range(1, 1001, 1)
        _generator = gen_lock(_original)

        _list = []

        def _yield_func():
            for item in _generator:
                _list.append(item)

        ts = [
            Thread(target=_yield_func),
            Thread(target=_yield_func),
            Thread(target=_yield_func),
            Thread(target=_yield_func),
        ]
        for t in ts:
            t.start()
        for t in ts:
            t.join()

        assert sorted(_list) == sorted(list(_original))


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
