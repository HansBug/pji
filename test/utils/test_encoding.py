import os
from typing import List, Union

import pytest

from pji.utils.encoding import auto_decode, auto_encode_support, auto_encode, auto_decode_support


@pytest.mark.unittest
class TestUtilsEncoding:
    def test_auto_encode(self):
        assert auto_encode('kdsfjldsjflkdsmgds') == b'kdsfjldsjflkdsmgds'

    def test_auto_decode(self):
        assert auto_decode(b'kdsfjldsjflkdsmgds') == 'kdsfjldsjflkdsmgds'
        assert auto_decode(bytearray(b'kdsfjldsjflkdsmgds')) == 'kdsfjldsjflkdsmgds'

        assert auto_decode(
            b'\xd0\x94\xd0\xbe\xd0\xb1\xd1\x80\xd1\x8b\xd0\xb9 '
            b'\xd0\xb2\xd0\xb5\xd1\x87\xd0\xb5\xd1\x80') == "Добрый вечер"
        assert auto_decode(b'\xa4\xb3\xa4\xf3\xa4\xd0\xa4\xf3\xa4\xcf') == "こんばんは"
        assert auto_decode(b'\xcd\xed\xc9\xcf\xba\xc3') == "晚上好"

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


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
