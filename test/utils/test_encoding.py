from typing import List, Union

import pytest

from pji.utils.encoding import auto_encode_support, auto_decode_support


@pytest.mark.unittest
class TestUtilsEncoding:
    # noinspection SpellCheckingInspection,PyTypeChecker
    def test_auto_encode_support(self):
        @auto_encode_support
        def _func(data: Union[bytes, bytearray]) -> int:
            assert not isinstance(data, str)
            return len(data)

        assert _func(bytes(12)) == 12
        assert _func(bytearray(12)) == 12
        assert _func('kdsfjldsjflkdsmgds') == 18

        with pytest.raises(TypeError):
            _func(None)

    def test_auto_decode_support(self):
        @auto_decode_support
        def _func_1(ls: List[int]) -> bytes:
            return bytes(ls)

        # noinspection PyTypeChecker
        @auto_decode_support
        def _func_2(ls: List[int]) -> str:
            return _func_1(ls)

        # noinspection PyUnusedLocal
        @auto_decode_support
        def _func_3(ls: List[int]) -> None:
            pass

        assert _func_1([115, 100, 115, 102, 108, 107, 115, 102, 100]) == 'sdsflksfd'
        assert _func_2([115, 100, 115, 102, 108, 107, 115, 102, 100]) == 'sdsflksfd'

        with pytest.raises(TypeError):
            _func_3([115, 100, 115, 102, 108, 107, 115, 102, 100])
