import codecs
import os
import tempfile

import pytest

from pji.service.command import CommandTemplate
from pji.service.section import CopyFileInputTemplate, CopyFileOutputTemplate, TagFileOutputTemplate, \
    StaticSectionInfoTemplate, LocalSectionInfoTemplate, TagSectionInfoTemplate, SectionCollectionTemplate, \
    SectionCollection
from pji.utils import FilePool
from .base import SECTION_TEMPLATE_1, SECTION_TEMPLATE_2, COMPLEX_TEXT, SECTION_TEMPLATE_FAILED_2, \
    SECTION_TEMPLATE_FAILED_1


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestServiceSectionSectionCollection:
    def test_template_simple(self):
        sct = SectionCollectionTemplate(SECTION_TEMPLATE_1, SECTION_TEMPLATE_2)

        assert len(sct.items) == 2
        assert sct.items[0].name == 'name_${V}'
        assert sct.items[1].name == 'name_2_${VT}'
        assert list(sct)[0].name == 'name_${V}'
        assert list(sct)[1].name == 'name_2_${VT}'
        assert repr(sct) == "<SectionCollectionTemplate sections: ('name_${V}', 'name_2_${VT}')>"

    def test_template_call(self):
        sct = SectionCollectionTemplate(SECTION_TEMPLATE_1, SECTION_TEMPLATE_2)

        with tempfile.TemporaryDirectory() as scriptdir:
            with codecs.open(os.path.join(scriptdir, 'README.md'), 'w') as of:
                of.write(COMPLEX_TEXT)
            sc = sct(
                scriptdir=scriptdir,
                identification='nobody',
                resources=dict(max_real_time='1.8s'),
                environ=dict(ENV='xxx', VF='123'),
            )

            assert isinstance(sc, SectionCollection)
            assert len(sc.getters) == 2
            assert len(list(sc)) == 2
            assert repr(sc) == "<SectionCollection sections: ('name_233', 'name_2_123233')>"

    def test_template_call_invalid(self):
        sct = SectionCollectionTemplate(SECTION_TEMPLATE_1, SECTION_TEMPLATE_2)

        with tempfile.TemporaryDirectory() as scriptdir:
            with codecs.open(os.path.join(scriptdir, 'README.md'), 'w') as of:
                of.write(COMPLEX_TEXT)

            with pytest.raises(KeyError):
                with FilePool() as pool:
                    sct(
                        pool=pool,
                        scriptdir=scriptdir,
                        identification='nobody',
                        resources=dict(max_real_time='1.8s'),
                        environ=dict(ENV='xxx', VF='123'),
                    )
            with pytest.raises(KeyError):
                sct(
                    scriptdir=scriptdir,
                    identification='nobody',
                    resources=dict(max_real_time='1.8s'),
                    environ=dict(ENV='xxx', V='123'),
                )

    def test_template_call_duplicate_names(self):
        sct = SectionCollectionTemplate(SECTION_TEMPLATE_1, SECTION_TEMPLATE_2, SECTION_TEMPLATE_FAILED_1)
        with tempfile.TemporaryDirectory() as scriptdir:
            with codecs.open(os.path.join(scriptdir, 'README.md'), 'w') as of:
                of.write(COMPLEX_TEXT)
            with pytest.raises(KeyError):
                sct(
                    scriptdir=scriptdir,
                    identification='nobody',
                    resources=dict(max_real_time='1.8s'),
                    environ=dict(ENV='xxx', VF='123'),
                )

    def test_template_loads(self):
        sct = SectionCollectionTemplate(SECTION_TEMPLATE_1, SECTION_TEMPLATE_2)
        assert SectionCollectionTemplate.loads(sct) is sct

        sctx = SectionCollectionTemplate.loads(SECTION_TEMPLATE_1)
        assert isinstance(sctx, SectionCollectionTemplate)
        assert len(sctx.items) == 1

        sctx = SectionCollectionTemplate.loads(dict(
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
        assert isinstance(sctx, SectionCollectionTemplate)
        assert len(sctx.items) == 1

        sctx = SectionCollectionTemplate.loads([dict(
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
        )])
        assert isinstance(sctx, SectionCollectionTemplate)
        assert len(sctx.items) == 1

        with pytest.raises(TypeError):
            SectionCollectionTemplate.loads(123)

    def test_collection_call(self):
        sct = SectionCollectionTemplate(SECTION_TEMPLATE_1, SECTION_TEMPLATE_2)

        with tempfile.TemporaryDirectory() as scriptdir:
            with codecs.open(os.path.join(scriptdir, 'README.md'), 'w') as of:
                of.write(COMPLEX_TEXT)
            sc = sct(
                scriptdir=scriptdir,
                identification='nobody',
                resources=dict(max_real_time='1.8s'),
                environ=dict(ENV='xxx', VF='123'),
            )

            _success, _results = sc()
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

    def test_collection_call_fail(self):
        sct = SectionCollectionTemplate(SECTION_TEMPLATE_1, SECTION_TEMPLATE_2, SECTION_TEMPLATE_FAILED_2)

        with tempfile.TemporaryDirectory() as scriptdir:
            with codecs.open(os.path.join(scriptdir, 'README.md'), 'w') as of:
                of.write(COMPLEX_TEXT)
            sc = sct(
                scriptdir=scriptdir,
                identification='nobody',
                resources=dict(max_real_time='1.8s'),
                environ=dict(ENV='xxx', VF='123'),
            )

            _success, _results = sc()
            assert not _success
            assert len(_results) == 3

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

            _name_3, (_section_3_success, _section_3_results, _section_3_info) = _results[2]
            assert _name_3 == 'name_f2_233'
            assert not _section_3_success
            assert len(_section_3_results) == 3
            assert _section_3_results[0].ok
            assert _section_3_results[1].ok
            assert not _section_3_results[2].ok
            assert _section_3_info == {
                'static': 'this is v : 233', 'value': 233,
                'local_1': '233 233\n', 'local_2': 'xxx 233\n',
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
            }


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
