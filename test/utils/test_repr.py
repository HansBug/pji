import os

import pytest

from pji.utils import get_repr_info


@pytest.mark.unittest
class TestUtilsRepr:
    def test_get_repr_info(self):
        class Sum:
            def __init__(self, a, b):
                self.__a = a
                self.__b = b

            def __repr__(self):
                return get_repr_info(
                    cls=self.__class__,
                    args=[
                        ('b', (lambda: self.__b, lambda: self.__b is not None)),
                        ('a', lambda: self.__a),
                    ]
                )

        assert repr(Sum(1, 2)) == '<Sum b: 2, a: 1>'
        assert repr(Sum(None, None)) == '<Sum a: None>'


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
