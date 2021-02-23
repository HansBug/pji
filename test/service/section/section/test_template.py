import os

import pytest

from pji.control.model import Identification, ResourceLimit
from pji.service.command import CommandTemplate, CommandCollectionTemplate
from pji.service.section import SectionTemplate, CopyFileInputTemplate, CopyFileOutputTemplate, TagFileOutputTemplate, \
    StaticSectionInfoTemplate, LocalSectionInfoTemplate, FileInputCollectionTemplate, FileOutputCollectionTemplate, \
    SectionInfoMappingTemplate


@pytest.mark.unittest
class TestServiceSectionSectionTemplate:
    def test_simple(self):
        st = SectionTemplate(
            name='name_${V}',
            commands=[
                CommandTemplate(args='echo 233 ${V}', stdout='stdout_1_${V}.txt', stderr='stderr_1_${V}.txt'),
                CommandTemplate(args='echo 2334 ${V} 1>&2', stdout='stdout_2_${V}.txt', stderr='stderr_2_${V}.txt'),
                CommandTemplate(args='cat ${V}/r.md', stdout='stdout_3_${V}.txt', stderr='stderr_3_${V}.txt'),
                CommandTemplate(args='base64 ${V}/r.md 1>&2', stdout='stdout_4_${V}.txt', stderr='stderr_4_${V}.txt'),
            ],
            identification='nobody',
            resources=dict(max_real_time='2.0s'),
            environ=dict(V='233'),
            inputs=[
                CopyFileInputTemplate(file='README.md', local='${V}/r.md', privilege='r--')
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
                'local': LocalSectionInfoTemplate('stdout_1_${V}.txt'),
                'tag': LocalSectionInfoTemplate('t_1_${V}'),
            }
        )

        assert st.name == 'name_${V}'
        assert st.identification == Identification.loads('nobody')
        assert st.resources == ResourceLimit.loads({'max_real_time': '2.0s'})
        assert st.environ == {'V': '233'}
        assert isinstance(st.commands, CommandCollectionTemplate)
        assert len(st.commands.commands) == 4
        assert isinstance(st.inputs, FileInputCollectionTemplate)
        assert len(st.inputs.inputs) == 1
        assert isinstance(st.outputs, FileOutputCollectionTemplate)
        assert len(st.outputs.outputs) == 4
        assert isinstance(st.infos, SectionInfoMappingTemplate)
        assert len(st.infos.mapping.keys()) == 4


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
