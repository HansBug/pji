import pytest
from pji.service.section.input.base import _load_privilege, InputCondition, _load_input_condition
from pysyslimit import FilePermission


@pytest.mark.unittest
class TestServiceSectionInputBase:
    def test_load_privilege(self):
        assert _load_privilege('rwx') == FilePermission.loads('rwx------')
        assert _load_privilege('664') == FilePermission.loads('rw-rw-r--')
        assert _load_privilege('rw-r-x-wx') == FilePermission.loads('rw-r-x-wx')
        assert _load_privilege('') is None
        assert _load_privilege(None) is None

    def test_load_input_condition(self):
        assert _load_input_condition('required') == InputCondition.REQUIRED
        assert _load_input_condition('optional') == InputCondition.OPTIONAL
        assert _load_input_condition('Required') == InputCondition.REQUIRED
        assert _load_input_condition('OPTIONAL') == InputCondition.OPTIONAL
        assert _load_input_condition(None) == InputCondition.REQUIRED
        assert _load_input_condition('') == InputCondition.REQUIRED
        with pytest.raises(KeyError):
            _ = _load_input_condition(3)
