from pji.service.command import CommandTemplate
from pji.service.section import SectionTemplate, CopyFileInputTemplate, CopyFileOutputTemplate, TagFileOutputTemplate, \
    StaticSectionInfoTemplate, LocalSectionInfoTemplate, TagSectionInfoTemplate, TagFileInputTemplate

COMPLEX_TEXT = """I have a dream that one day, down in Alabama, with its vicious racists, 
with its governor having his lips dripping with the words of "interposition" and "nullification"
 -- one day right there in Alabama little black boys and black girls will be able to join 
 hands with little white boys and white girls as sisters and brothers."""

# noinspection DuplicatedCode
SECTION_TEMPLATE_1 = SectionTemplate(
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
    },
    info_dump='info.txt',
)

SECTION_TEMPLATE_2 = SectionTemplate(
    name='name_2_${VT}',
    commands=[
        CommandTemplate(args='whoami', stdout='stdout_5_${VT}.txt', stderr='stderr_5_${VT}.txt'),
        CommandTemplate(args='base64 stdout_3_${V}.txt', stdout='stdout_6_${VT}.txt', stderr='stderr_6_${VT}.txt'),
        CommandTemplate(args='base64 stdout_4_${V}.txt 1>&2', stdout='stdout_7_${VT}.txt', stderr='stderr_7_${VT}.txt'),
    ],
    identification='sys',
    resources=dict(max_real_time='2.0s'),
    environ=dict(V='233', VT='${VF}233'),
    inputs=[
        CopyFileInputTemplate(file='README.md', local='${V}/r.md', privilege='r-x'),
        TagFileInputTemplate(tag='t_1_${V}', local='stdout_3_${V}.txt', privilege='r--'),
        TagFileInputTemplate(tag='t_2_${V}', local='stdout_4_${V}.txt', privilege='r--'),
    ],
    outputs=[
        TagFileOutputTemplate(local='stdout_5_${VT}.txt', tag='t_3_${VT}'),
        TagFileOutputTemplate(local='stdout_6_${VT}.txt', tag='t_4_${VT}'),
        TagFileOutputTemplate(local='stderr_7_${VT}.txt', tag='t_5_${VT}'),
    ],
    infos={
        'static': StaticSectionInfoTemplate('this is vt : ${VT}'),
        'tag_1': TagSectionInfoTemplate('t_1_${V}'),
        'tag_2': TagSectionInfoTemplate('t_2_${V}'),
        'tag_3t': TagSectionInfoTemplate('t_3_${VT}'),
        'tag_4t': TagSectionInfoTemplate('t_4_${VT}'),
        'tag_5t': TagSectionInfoTemplate('t_5_${VT}'),
    }
)

SECTION_TEMPLATE_FAILED_1 = SectionTemplate(
    name='name_${V}',
    commands=[
        CommandTemplate(args='echo 233 ${V}', stdout='stdout_1_${V}.txt', stderr='stderr_1_${V}.txt'),
        CommandTemplate(args='echo ${ENV} ${V} 1>&2', stdout='stdout_2_${V}.txt', stderr='stderr_2_${V}.txt'),
        CommandTemplate(args='false'),
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
        TagFileOutputTemplate(local='stdout_1_${V}.txt', tag='t_1_${V}'),
        TagFileOutputTemplate(local='stderr_2_${V}.txt', tag='t_2_${V}'),
    ],
    infos={
        'static': StaticSectionInfoTemplate('this is v : ${V}'),
        'value': StaticSectionInfoTemplate(233),
        'local_1': LocalSectionInfoTemplate('stdout_1_${V}.txt'),
        'local_2': LocalSectionInfoTemplate('stderr_2_${V}.txt'),
        'tag_1': TagSectionInfoTemplate('t_1_${V}'),
        'tag_2': TagSectionInfoTemplate('t_2_${V}'),
    }
)

SECTION_TEMPLATE_FAILED_2 = SectionTemplate(
    name='name_f2_${V}',
    commands=[
        CommandTemplate(args='echo 233 ${V}', stdout='stdout_1_${V}.txt', stderr='stderr_1_${V}.txt'),
        CommandTemplate(args='echo ${ENV} ${V} 1>&2', stdout='stdout_2_${V}.txt', stderr='stderr_2_${V}.txt'),
        CommandTemplate(args='false'),
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
        TagFileOutputTemplate(local='stdout_1_${V}.txt', tag='t_1_${V}'),
        TagFileOutputTemplate(local='stderr_2_${V}.txt', tag='t_2_${V}'),
    ],
    infos={
        'static': StaticSectionInfoTemplate('this is v : ${V}'),
        'value': StaticSectionInfoTemplate(233),
        'local_1': LocalSectionInfoTemplate('stdout_1_${V}.txt'),
        'local_2': LocalSectionInfoTemplate('stderr_2_${V}.txt'),
        'tag_1': TagSectionInfoTemplate('t_1_${V}'),
        'tag_2': TagSectionInfoTemplate('t_2_${V}'),
    }
)
