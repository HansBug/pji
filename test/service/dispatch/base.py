from pji.service.dispatch import DispatchTemplate
from ..task.base import TASK_TEMPLATE_SUCCESS_1, TASK_TEMPLATE_SUCCESS_2, TASK_TEMPLATE_FAILURE_1

DISPATCH_TEMPLATE = DispatchTemplate(
    global_=dict(
        environ=dict(V='233', K='tc', VF='gtc', PATH='/root/bin:${PATH}'),
        use_sys_env=['PATH'],
    ),
    tasks=[
        TASK_TEMPLATE_SUCCESS_1,
        TASK_TEMPLATE_SUCCESS_2,
        TASK_TEMPLATE_FAILURE_1,
    ]
)
