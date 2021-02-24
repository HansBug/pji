import codecs
import os
import tempfile

import pytest

from pji.control.model import Identification, ResourceLimit
from .base import TASK_TEMPLATE_SUCCESS_1, TASK_TEMPLATE_SUCCESS_2
from ..section.section.base import COMPLEX_TEXT


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestServiceTaskTask:
    def test_task_simple(self):
        tt = TASK_TEMPLATE_SUCCESS_1

        with tempfile.TemporaryDirectory() as scriptdir:
            with codecs.open(os.path.join(scriptdir, 'README.md'), 'w') as of:
                of.write(COMPLEX_TEXT)

            t = tt(
                scriptdir=scriptdir,
                resources=dict(max_real_time='1.0s'),
                environ=dict(K='233'),
            )

            assert t.name == 'task_x233x'
            assert t.identification == Identification.loads('nobody')
            assert t.resources == ResourceLimit.loads(dict(max_real_time='1.0s'))
            assert t.environ == {'K': '233', 'NAME': 'x233x', 'PJI_TASK_NAME': 'task_x233x'}
            assert len(t.sections.getters) == 1
            assert repr(t) == "<Task name: 'task_x233x', identification: <Identification user: nobody, " \
                              "group: nogroup>, resources: <ResourceLimit real time: 1.000s>, " \
                              "sections: <SectionCollection sections: ('name_233',)>>"

    def test_task_invalid(self):
        tt = TASK_TEMPLATE_SUCCESS_1

        with tempfile.TemporaryDirectory() as scriptdir:
            with codecs.open(os.path.join(scriptdir, 'README.md'), 'w') as of:
                of.write(COMPLEX_TEXT)
            with pytest.raises(ValueError):
                tt(
                    scriptdir=scriptdir,
                    resources=dict(max_real_time='1.0s'),
                    environ=dict(K='???'),
                )

    def test_task_call(self):
        tt = TASK_TEMPLATE_SUCCESS_2

        with tempfile.TemporaryDirectory() as scriptdir:
            with codecs.open(os.path.join(scriptdir, 'README.md'), 'w') as of:
                of.write(COMPLEX_TEXT)

            t = tt(
                scriptdir=scriptdir,
                resources=dict(max_real_time='1.0s'),
                environ=dict(K='233', ENV='xxx', VF='123'),
            )

            _success, _results = t()
            assert _success

            _name_1, (_section_1_success, _section_1_results, _section_1_info) = _results[0]
            assert _name_1 == 'name_233'
            assert _section_1_success
            assert len(_section_1_results) == 4
            assert _section_1_results[0].ok
            assert _section_1_results[1].ok
            assert _section_1_results[2].ok
            assert _section_1_results[3].ok
            assert _section_1_info == {'static': 'this is v : 233', 'value': 233,
                                       'local': 'I have a dream that one day, down in Alabama, with its '
                                                'vicious racists, \nwith its governor having his lips '
                                                'dripping with the words of "interposition" and "nullification"\n'
                                                ' -- one day right there in Alabama little black boys and black '
                                                'girls will be able to join \n hands with little white boys and '
                                                'white girls as sisters and brothers.',
                                       'tag': 'I have a dream that one day, down in Alabama, with its vicious '
                                              'racists, \nwith its governor having his lips dripping with the '
                                              'words of "interposition" and "nullification"\n -- one day right '
                                              'there in Alabama little black boys and black girls will be able to '
                                              'join \n hands with little white boys and white girls as sisters '
                                              'and brothers.',
                                       'base64': 'SSBoYXZlIGEgZHJlYW0gdGhhdCBvbmUgZGF5LCBkb3duIGluIEFsYWJhbWEsIHd'
                                                 'pdGggaXRzIHZp\nY2lvdXMgcmFjaXN0cywgCndpdGggaXRzIGdvdmVybm9yIGhh'
                                                 'dmluZyBoaXMgbGlwcyBkcmlwcGlu\nZyB3aXRoIHRoZSB3b3JkcyBvZiAiaW50Z'
                                                 'XJwb3NpdGlvbiIgYW5kICJudWxsaWZpY2F0aW9uIgog\nLS0gb25lIGRheSByaW'
                                                 'dodCB0aGVyZSBpbiBBbGFiYW1hIGxpdHRsZSBibGFjayBib3lzIGFuZCBi\nbGF'
                                                 'jayBnaXJscyB3aWxsIGJlIGFibGUgdG8gam9pbiAKIGhhbmRzIHdpdGggbGl0dG'
                                                 'xlIHdoaXRl\nIGJveXMgYW5kIHdoaXRlIGdpcmxzIGFzIHNpc3RlcnMgYW5kIGJ'
                                                 'yb3RoZXJzLg==\n'}

            _name_2, (_section_2_success, _section_2_results, _section_2_info) = _results[1]
            assert _name_2 == 'name_2_123233'
            assert _section_2_success
            assert len(_section_2_results) == 3
            assert _section_2_results[0].ok
            assert _section_2_results[1].ok
            assert _section_2_results[2].ok
            assert _section_2_info == {'static': 'this is vt : 123233',
                                       'tag_1': 'I have a dream that one day, down in Alabama, with its vicious '
                                                'racists, \nwith its governor having his lips dripping with the '
                                                'words of "interposition" and "nullification"\n -- one day right '
                                                'there in Alabama little black boys and black girls will be able '
                                                'to join \n hands with little white boys and white girls as sisters '
                                                'and brothers.',
                                       'tag_2': 'SSBoYXZlIGEgZHJlYW0gdGhhdCBvbmUgZGF5LCBkb3duIGluIEFsYWJhbWEsIHdpdGgg'
                                                'aXRzIHZp\nY2lvdXMgcmFjaXN0cywgCndpdGggaXRzIGdvdmVybm9yIGhhdmluZyBoaX'
                                                'MgbGlwcyBkcmlwcGlu\nZyB3aXRoIHRoZSB3b3JkcyBvZiAiaW50ZXJwb3NpdGlvbiIg'
                                                'YW5kICJudWxsaWZpY2F0aW9uIgog\nLS0gb25lIGRheSByaWdodCB0aGVyZSBpbiBBbG'
                                                'FiYW1hIGxpdHRsZSBibGFjayBib3lzIGFuZCBi\nbGFjayBnaXJscyB3aWxsIGJlIGFi'
                                                'bGUgdG8gam9pbiAKIGhhbmRzIHdpdGggbGl0dGxlIHdoaXRl\nIGJveXMgYW5kIHdoaX'
                                                'RlIGdpcmxzIGFzIHNpc3RlcnMgYW5kIGJyb3RoZXJzLg==\n',
                                       'tag_3t': 'sys\n',
                                       'tag_4t': 'SSBoYXZlIGEgZHJlYW0gdGhhdCBvbmUgZGF5LCBkb3duIGluIEFsYWJhbWEsIHdpdGg'
                                                 'gaXRzIHZp\nY2lvdXMgcmFjaXN0cywgCndpdGggaXRzIGdvdmVybm9yIGhhdmluZyBo'
                                                 'aXMgbGlwcyBkcmlwcGlu\nZyB3aXRoIHRoZSB3b3JkcyBvZiAiaW50ZXJwb3NpdGlvb'
                                                 'iIgYW5kICJudWxsaWZpY2F0aW9uIgog\nLS0gb25lIGRheSByaWdodCB0aGVyZSBpbi'
                                                 'BBbGFiYW1hIGxpdHRsZSBibGFjayBib3lzIGFuZCBi\nbGFjayBnaXJscyB3aWxsIGJ'
                                                 'lIGFibGUgdG8gam9pbiAKIGhhbmRzIHdpdGggbGl0dGxlIHdoaXRl\nIGJveXMgYW5k'
                                                 'IHdoaXRlIGdpcmxzIGFzIHNpc3RlcnMgYW5kIGJyb3RoZXJzLg==\n',
                                       'tag_5t': 'U1NCb1lYWmxJR0VnWkhKbFlXMGdkR2hoZENCdmJtVWdaR0Y1TENCa2IzZHVJR2x1SUV'
                                                 'Gc1lXSmhi\nV0VzSUhkcGRHZ2dhWFJ6SUhacApZMmx2ZFhNZ2NtRmphWE4wY3l3Z0Nu'
                                                 'ZHBkR2dnYVhSeklHZHZk\nbVZ5Ym05eUlHaGhkbWx1WnlCb2FYTWdiR2x3Y3lCa2Ntb'
                                                 'HdjR2x1Clp5QjNhWFJvSUhSb1pTQjNi\nM0prY3lCdlppQWlhVzUwWlhKd2IzTnBkR2'
                                                 'x2YmlJZ1lXNWtJQ0p1ZFd4c2FXWnBZMkYwYVc5dUln\nb2cKTFMwZ2IyNWxJR1JoZVN'
                                                 'CeWFXZG9kQ0IwYUdWeVpTQnBiaUJCYkdGaVlXMWhJR3hwZEhSc1pT\nQmliR0ZqYXlC'
                                                 'aWIzbHpJR0Z1WkNCaQpiR0ZqYXlCbmFYSnNjeUIzYVd4c0lHSmxJR0ZpYkdVZ2RH\nO'
                                                 'GdhbTlwYmlBS0lHaGhibVJ6SUhkcGRHZ2diR2wwZEd4bElIZG9hWFJsCklHSnZlWE1n'
                                                 'WVc1a0lI\nZG9hWFJsSUdkcGNteHpJR0Z6SUhOcGMzUmxjbk1nWVc1a0lHSnliM1JvW'
                                                 'lhKekxnPT0K\n'}


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
