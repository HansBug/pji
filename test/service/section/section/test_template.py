import os

import pytest

from pji.control.model import Identification, ResourceLimit
from pji.service.command import CommandCollectionTemplate
from pji.service.section import FileInputCollectionTemplate, FileOutputCollectionTemplate, \
    SectionInfoMappingTemplate, SectionTemplate
from .base import _SECTION_TEMPLATE


@pytest.mark.unittest
class TestServiceSectionSectionTemplate:
    __DEMO_TEMPLATE = _SECTION_TEMPLATE

    def test_template_simple(self):
        assert self.__DEMO_TEMPLATE.name == 'name_${V}'
        assert self.__DEMO_TEMPLATE.identification == Identification.loads('nobody')
        assert self.__DEMO_TEMPLATE.resources == ResourceLimit.loads({'max_real_time': '2.0s'})
        assert self.__DEMO_TEMPLATE.environ == {'V': '233'}
        assert isinstance(self.__DEMO_TEMPLATE.commands, CommandCollectionTemplate)
        assert len(self.__DEMO_TEMPLATE.commands.commands) == 4
        assert isinstance(self.__DEMO_TEMPLATE.inputs, FileInputCollectionTemplate)
        assert len(self.__DEMO_TEMPLATE.inputs.items) == 1
        assert isinstance(self.__DEMO_TEMPLATE.outputs, FileOutputCollectionTemplate)
        assert len(self.__DEMO_TEMPLATE.outputs.items) == 4
        assert isinstance(self.__DEMO_TEMPLATE.infos, SectionInfoMappingTemplate)
        assert len(self.__DEMO_TEMPLATE.infos.items.keys()) == 5

        assert repr(self.__DEMO_TEMPLATE) == "<SectionTemplate name: 'name_${V}', " \
                                             "identification: <Identification user: nobody, " \
                                             "group: nogroup>, resources: <ResourceLimit real time: 2.000s>, " \
                                             "inputs: 1, outputs: 4, infos: 5, commands: 4>"

    def test_loads(self):
        assert SectionTemplate.loads(_SECTION_TEMPLATE) == _SECTION_TEMPLATE
        with pytest.raises(TypeError):
            SectionTemplate.loads([])


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
