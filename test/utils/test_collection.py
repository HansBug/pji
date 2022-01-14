import pytest

from pji.utils import duplicates


@pytest.mark.unittest
class TestUtilsCollection:
    def test_duplicates(self):
        assert duplicates([1, 2, 3]) == set()
        assert duplicates({1, 2, 3}) == set()
        assert duplicates((1, 2, 3)) == set()
        assert duplicates([1, 2, 3, 2, 3]) == {2, 3}
        assert duplicates((1, 2, 3, 2, 3)) == {2, 3}
