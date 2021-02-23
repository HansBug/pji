import os

import pytest

from pji.control.model import Identification, ResourceLimit
from pji.service.command import CommandCollectionTemplate, CommandTemplate
from pji.service.section import CopyFileInputTemplate, CopyFileOutputTemplate, TagFileOutputTemplate, \
    StaticSectionInfoTemplate, LocalSectionInfoTemplate, TagSectionInfoTemplate, FileInputCollectionTemplate, \
    FileOutputCollectionTemplate, \
    SectionInfoMappingTemplate, SectionTemplate
from .base import _SECTION_TEMPLATE


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestServiceSectionSectionTemplate:
    def test_template_simple(self):
        assert _SECTION_TEMPLATE.name == 'name_${V}'
        assert _SECTION_TEMPLATE.identification == Identification.loads('nobody')
        assert _SECTION_TEMPLATE.resources == ResourceLimit.loads({'max_real_time': '2.0s'})
        assert _SECTION_TEMPLATE.environ == {'V': '233'}
        assert isinstance(_SECTION_TEMPLATE.commands, CommandCollectionTemplate)
        assert len(_SECTION_TEMPLATE.commands.commands) == 4
        assert isinstance(_SECTION_TEMPLATE.inputs, FileInputCollectionTemplate)
        assert len(_SECTION_TEMPLATE.inputs.items) == 1
        assert isinstance(_SECTION_TEMPLATE.outputs, FileOutputCollectionTemplate)
        assert len(_SECTION_TEMPLATE.outputs.items) == 4
        assert isinstance(_SECTION_TEMPLATE.infos, SectionInfoMappingTemplate)
        assert len(_SECTION_TEMPLATE.infos.items.keys()) == 5

        assert repr(_SECTION_TEMPLATE) == "<SectionTemplate name: 'name_${V}', " \
                                          "identification: <Identification user: nobody, " \
                                          "group: nogroup>, resources: <ResourceLimit real time: 2.000s>, " \
                                          "inputs: 1, outputs: 4, infos: 5, commands: 4>"

    def test_loads(self):
        assert SectionTemplate.loads(_SECTION_TEMPLATE) == _SECTION_TEMPLATE

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
