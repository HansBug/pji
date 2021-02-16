import os

import pytest

from pji.utils.encoding import *


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


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
