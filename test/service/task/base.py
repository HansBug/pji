from pji.service.task import TaskTemplate
from ..section.section.base import SECTION_TEMPLATE_1, SECTION_TEMPLATE_2, SECTION_TEMPLATE_FAILED_2

TASK_TEMPLATE_SUCCESS_1 = TaskTemplate(
    name='task1_${NAME}',
    identification='nobody',
    resources=dict(max_real_time='1.5s'),
    environ=dict(NAME='x${K}x'),
    sections=[
        SECTION_TEMPLATE_1,
    ]
)

TASK_TEMPLATE_SUCCESS_2 = TaskTemplate(
    name='task2_${NAME}',
    identification='nobody',
    resources=dict(max_real_time='1.5s'),
    environ=dict(NAME='x${K}x'),
    sections=[
        SECTION_TEMPLATE_1,
        SECTION_TEMPLATE_2,
    ]
)

TASK_TEMPLATE_FAILURE_1 = TaskTemplate(
    name='task3_${NAME}',
    identification='nobody',
    resources=dict(max_real_time='1.5s'),
    environ=dict(NAME='x${K}x'),
    sections=[
        SECTION_TEMPLATE_1,
        SECTION_TEMPLATE_2,
        SECTION_TEMPLATE_FAILED_2,
    ]
)
