import pytest
from pysyslimit import FilePermission

from pji.service.section.input.base import _load_privilege


@pytest.mark.unittest
class TestServiceSectionInputBase:
    def test_load_privilege(self):
        assert _load_privilege('rwx') == FilePermission.loads('rwx------')
        assert _load_privilege('664') == FilePermission.loads('rw-rw-r--')
        assert _load_privilege('rw-r-x-wx') == FilePermission.loads('rw-r-x-wx')
        assert _load_privilege('') is None
        assert _load_privilege(None) is None
