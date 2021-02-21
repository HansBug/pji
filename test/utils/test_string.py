import os

import pytest

from pji.utils import env_template


@pytest.mark.unittest
class TestUtilsString:
    def test_env_template(self):
        assert env_template('sdkjflsd') == 'sdkjflsd'
        assert env_template('this is the ${number} day.', dict(number='1st')) == 'this is the 1st day.'
        with pytest.raises(KeyError):
            env_template('this is the ${number} day')


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
