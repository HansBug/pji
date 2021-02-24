import os

import pytest

from pji.control.model import Identification, ResourceLimit
from pji.service.task import TaskTemplate
from .base import TASK_TEMPLATE_SUCCESS_1, SECTION_1_TEMPLATE


@pytest.mark.unittest
class TestServiceTaskTemplate:
    def test_template_simple(self):
        tt = TASK_TEMPLATE_SUCCESS_1

        assert tt.name == 'task_${NAME}'
        assert tt.identification == Identification.loads('nobody')
        assert tt.resources == ResourceLimit.loads(dict(max_real_time='1.5s'))
        assert tt.environ == dict(NAME='x${K}x')
        assert len(tt.sections.items) == 1

    def test_loads(self):
        assert TaskTemplate.loads(TASK_TEMPLATE_SUCCESS_1) == TASK_TEMPLATE_SUCCESS_1
        assert len(TaskTemplate.loads(dict(
            name='task_${NAME}',
            identification='nobody',
            resources=dict(max_real_time='1.5s'),
            environ=dict(NAME='x${K}x'),
            sections=[
                SECTION_1_TEMPLATE,
            ]
        )).sections.items) == 1
        assert TaskTemplate.loads(('task_${NAME}', dict(
            identification='nobody',
            resources=dict(max_real_time='1.5s'),
            environ=dict(NAME='x${K}x'),
            sections=[
                SECTION_1_TEMPLATE,
            ]
        ))).name == 'task_${NAME}'

        with pytest.warns(RuntimeWarning):
            assert TaskTemplate.loads(('task_${NAME}', dict(
                name='task_2_${NAME}',
                identification='nobody',
                resources=dict(max_real_time='1.5s'),
                environ=dict(NAME='x${K}x'),
                sections=[
                    SECTION_1_TEMPLATE,
                ]
            ))).name == 'task_${NAME}'

    def test_loads_invalid(self):
        with pytest.raises(TypeError):
            TaskTemplate.loads(('name', []))
        with pytest.raises(TypeError):
            TaskTemplate.loads(233)


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
