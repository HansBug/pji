import os

import pytest

from pji.utils import env_template, truncate


@pytest.mark.unittest
class TestUtilsString:
    def test_env_template(self):
        assert env_template('sdkjflsd') == 'sdkjflsd'
        assert env_template('this is the ${number} day.', dict(number='1st')) == 'this is the 1st day.'
        with pytest.raises(KeyError):
            env_template('this is the ${number} day')

    def test_truncate(self):
        assert truncate(
            'this is the first time we do this kind of thing') == 'this is the first time we do this kind of thing'
        assert truncate('this is the first time we do this kind of thing', width=30) == 'this is the first time we ... '
        assert truncate('this is the first time we do this kind of thing', width=40, tail_length=12,
                        show_length=True) == 'this is the ..(47 chars).. ind of thing'


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
