import codecs
import os
import tempfile

import pytest

from pji.service.dispatch import Dispatch, DispatchTemplate
from .base import DISPATCH_TEMPLATE, TASK_TEMPLATE_SUCCESS_1, TASK_TEMPLATE_SUCCESS_2, TASK_TEMPLATE_FAILURE_1
from ..section.section.base import COMPLEX_TEXT


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestServiceDispatchDispatch:
    def test_template_simple(self):
        dt = DISPATCH_TEMPLATE
        assert set(dt.tasks.items.keys()) == {'task2_${NAME}', 'task3_${NAME}', 'task1_${NAME}'}
        assert dt.global_.environ == {
            'K': 'tc', 'V': '233', 'VF': 'gtc',
            'PATH': '/root/bin:${PATH}',
        }
        assert repr(dt) == "<DispatchTemplate tasks: ('task1_${NAME}', 'task2_${NAME}', 'task3_${NAME}')>"

    def test_template_call(self):
        d = DISPATCH_TEMPLATE(scriptdir='.')
        assert isinstance(d, Dispatch)
        assert d.global_.environ == {
            'K': 'tc', 'V': '233', 'VF': 'gtc',
            'PATH': '/root/bin:' + os.environ['PATH'],
        }
        assert set(d.tasks.items.keys()) == {'task3_xtcx', 'task1_xtcx', 'task2_xtcx'}
        assert repr(d) == "<Dispatch tasks: ('task1_xtcx', 'task2_xtcx', 'task3_xtcx')>"

    def test_template_loads(self):
        assert DispatchTemplate.loads(DISPATCH_TEMPLATE) == DISPATCH_TEMPLATE
        assert DispatchTemplate.loads({
            'global': dict(
                environ=dict(V='233', K='tc', VF='gtc', PATH='/root/bin:${PATH}'),
                use_sys_env=['PATH'],
            ),
            'tasks': [
                TASK_TEMPLATE_SUCCESS_1,
                TASK_TEMPLATE_SUCCESS_2,
                TASK_TEMPLATE_FAILURE_1,
            ],
        }).global_.environ == {
                   'K': 'tc', 'V': '233', 'VF': 'gtc',
                   'PATH': '/root/bin:${PATH}',
               }
        with pytest.raises(TypeError):
            DispatchTemplate.loads(123)

    def test_dispatch_call(self):
        with tempfile.TemporaryDirectory() as scriptdir:
            with codecs.open(os.path.join(scriptdir, 'README.md'), 'w') as of:
                of.write(COMPLEX_TEXT)
            d = DISPATCH_TEMPLATE(scriptdir=scriptdir)

            _success, _results = d('task2_xtcx')
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
            assert _name_2 == 'name_2_gtc233'
            assert _section_2_success
            assert len(_section_2_results) == 3
            assert _section_2_results[0].ok
            assert _section_2_results[1].ok
            assert _section_2_results[2].ok
            assert _section_2_info == {'static': 'this is vt : gtc233',
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
