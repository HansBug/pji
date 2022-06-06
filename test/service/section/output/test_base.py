import pytest

from pji.service.section.output.base import ResultCondition


@pytest.mark.unittest
class TestServiceSectionOutputBase:
    def test_result_condition(self):
        assert ResultCondition.SUCCESS.need_run(True)
        assert not ResultCondition.SUCCESS.need_run(False)
        assert not ResultCondition.FAIL.need_run(True)
        assert ResultCondition.FAIL.need_run(False)
        assert ResultCondition.ALL.need_run(True)
        assert ResultCondition.ALL.need_run(False)
