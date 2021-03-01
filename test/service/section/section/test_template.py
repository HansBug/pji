import os

import pytest

from pji.control.model import Identification, ResourceLimit
from pji.service.command import CommandCollectionTemplate, CommandTemplate
from pji.service.section import CopyFileInputTemplate, CopyFileOutputTemplate, TagFileOutputTemplate, \
    StaticSectionInfoTemplate, LocalSectionInfoTemplate, TagSectionInfoTemplate, FileInputCollectionTemplate, \
    FileOutputCollectionTemplate, \
    SectionInfoMappingTemplate, SectionTemplate
from .base import SECTION_TEMPLATE_1


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestServiceSectionSectionTemplate:
    def test_template_simple(self):
        assert SECTION_TEMPLATE_1.name == 'name_${V}'
        assert SECTION_TEMPLATE_1.identification == Identification.loads('nobody')
        assert SECTION_TEMPLATE_1.resources == ResourceLimit.loads({'max_real_time': '2.0s'})
        assert SECTION_TEMPLATE_1.environ == {'V': '233'}
        assert isinstance(SECTION_TEMPLATE_1.commands, CommandCollectionTemplate)
        assert len(SECTION_TEMPLATE_1.commands.commands) == 4
        assert isinstance(SECTION_TEMPLATE_1.inputs, FileInputCollectionTemplate)
        assert len(SECTION_TEMPLATE_1.inputs.items) == 1
        assert isinstance(SECTION_TEMPLATE_1.outputs, FileOutputCollectionTemplate)
        assert len(SECTION_TEMPLATE_1.outputs.items) == 4
        assert isinstance(SECTION_TEMPLATE_1.infos, SectionInfoMappingTemplate)
        assert len(SECTION_TEMPLATE_1.infos.items.keys()) == 5
        assert SECTION_TEMPLATE_1.info_dump == 'info.txt'

        assert repr(SECTION_TEMPLATE_1) == "<SectionTemplate name: 'name_${V}', " \
                                           "identification: <Identification user: nobody, " \
                                           "group: nogroup>, resources: <ResourceLimit real time: 2.000s>, " \
                                           "inputs: 1, outputs: 4, infos: 5, commands: 4>"

    def test_loads(self):
        assert SectionTemplate.loads(SECTION_TEMPLATE_1) == SECTION_TEMPLATE_1

        c = SectionTemplate.loads(dict(
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
        ))
        assert c.name == 'name_${V}'
        assert c.identification == Identification.loads('nobody')
        assert c.resources == ResourceLimit.loads({'max_real_time': '2.0s'})
        assert c.environ == {'V': '233'}
        assert isinstance(c.commands, CommandCollectionTemplate)
        assert len(c.commands.commands) == 4
        assert isinstance(c.inputs, FileInputCollectionTemplate)
        assert len(c.inputs.items) == 1
        assert isinstance(c.outputs, FileOutputCollectionTemplate)
        assert len(c.outputs.items) == 4
        assert isinstance(c.infos, SectionInfoMappingTemplate)
        assert len(c.infos.items.keys()) == 5
        with pytest.raises(TypeError):
            SectionTemplate.loads([])


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
