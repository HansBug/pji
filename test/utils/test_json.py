import io
import json
import os
import tempfile

import pytest
import yaml
from yaml.parser import ParserError as YamlParserError

from pji.utils import auto_load_json, JsonLoadError


@pytest.mark.unittest
class TestUtilsJson:
    def test_auto_load_json(self):
        with io.BytesIO(json.dumps({'a': 233, 'b': -1}).encode()) as f:
            assert auto_load_json(f) == {'a': 233, 'b': -1}

        with io.BytesIO(yaml.safe_dump({'a': 233, 'b': -1}).encode()) as f:
            assert auto_load_json(f) == {'a': 233, 'b': -1}

    def test_auto_load_json_invalid(self):
        with pytest.raises(JsonLoadError) as ei:
            with io.BytesIO(b'[this]is invalid') as f:
                auto_load_json(f)

        err = ei.value
        assert isinstance(err.exception, YamlParserError)

    def test_auto_load_json_with_real_file(self):
        with tempfile.NamedTemporaryFile('w') as tmpfile:
            json.dump({'a': 233, 'b': -1}, tmpfile)
            tmpfile.flush()
            with open(tmpfile.name, 'rb') as file:
                assert auto_load_json(file) == {'a': 233, 'b': -1}

        with tempfile.NamedTemporaryFile('w') as tmpfile:
            yaml.safe_dump({'a': 233, 'b': -1}, tmpfile)
            tmpfile.flush()
            with open(tmpfile.name, 'rb') as file:
                assert auto_load_json(file) == {'a': 233, 'b': -1}


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
