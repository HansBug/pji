from pji.service.task import TaskTemplate
from ..section.section.base import SECTION_1_TEMPLATE, SECTION_2_TEMPLATE, SECTION_FAILED_2_TEMPLATE

TASK_TEMPLATE_SUCCESS_1 = TaskTemplate(
    name='task_${NAME}',
    identification='nobody',
    resources=dict(max_real_time='1.5s'),
    environ=dict(NAME='x${K}x'),
    sections=[
        SECTION_1_TEMPLATE,
    ]
)

TASK_TEMPLATE_SUCCESS_2 = TaskTemplate(
    name='task_${NAME}',
    identification='nobody',
    resources=dict(max_real_time='1.5s'),
    environ=dict(NAME='x${K}x'),
    sections=[
        SECTION_1_TEMPLATE,
        SECTION_2_TEMPLATE,
    ]
)

TASK_TEMPLATE_FAILURE_1 = TaskTemplate(
    name='task_${NAME}',
    identification='nobody',
    resources=dict(max_real_time='1.5s'),
    environ=dict(NAME='x${K}x'),
    sections=[
        SECTION_1_TEMPLATE,
        SECTION_2_TEMPLATE,
        SECTION_FAILED_2_TEMPLATE,
    ]
)
