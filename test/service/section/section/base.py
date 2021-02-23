from pji.service.command import CommandTemplate
from pji.service.section import SectionTemplate, CopyFileInputTemplate, CopyFileOutputTemplate, TagFileOutputTemplate, \
    StaticSectionInfoTemplate, LocalSectionInfoTemplate, TagSectionInfoTemplate

_SECTION_TEMPLATE = SectionTemplate(
    name='name_${V}',
    commands=[
        CommandTemplate(args='echo 233 ${V}', stdout='stdout_1_${V}.txt', stderr='stderr_1_${V}.txt'),
        CommandTemplate(args='echo ${ENV} ${V} 1>&2', stdout='stdout_2_${V}.txt', stderr='stderr_2_${V}.txt'),
        CommandTemplate(args='cat ${V}/r.md', stdout='stdout_3_${V}.txt', stderr='stderr_3_${V}.txt'),
        CommandTemplate(args='base64 ${V}/r.md 1>&2', stdout='stdout_4_${V}.txt', stderr='stderr_4_${V}.txt'),
    ],
    identification='nobody',
    resources=dict(max_real_time='2.0s'),
    environ=dict(V='233'),
    inputs=[
        CopyFileInputTemplate(file='README.md', local='${V}/r.md', privilege='r-x')
    ],
    outputs=[
        CopyFileOutputTemplate(local='stdout_1_${V}.txt', file='f1.txt'),
        CopyFileOutputTemplate(local='stderr_2_${V}.txt', file='f2.txt'),
        TagFileOutputTemplate(local='stdout_3_${V}.txt', tag='t_1_${V}'),
        TagFileOutputTemplate(local='stderr_4_${V}.txt', tag='t_2_${V}'),
    ],
    infos={
        'static': StaticSectionInfoTemplate('this is v : ${V}'),
        'value': StaticSectionInfoTemplate(233),
        'local': LocalSectionInfoTemplate('stdout_3_${V}.txt'),
        'tag': TagSectionInfoTemplate('t_1_${V}'),
        'base64': LocalSectionInfoTemplate('stderr_4_${V}.txt'),
    }
)
