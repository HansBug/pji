import codecs
import os
import tempfile

import pytest

from pji.control.model import Identification, ResourceLimit
from pji.utils import FilePool
from .base import _SECTION_1_TEMPLATE, _SECTION_FAILED_TEMPLATE, _COMPLEX_TEXT


@pytest.mark.unittest
class TestServiceSectionSectionSection:
    def test_section_simple(self):
        with tempfile.TemporaryDirectory() as scriptdir, \
                FilePool() as pool:
            with codecs.open(os.path.join(scriptdir, 'README.md'), 'w') as of:
                of.write(_COMPLEX_TEXT)
            s = _SECTION_1_TEMPLATE(
                scriptdir=scriptdir,
                pool=pool,
                identification='nobody',
                resources=dict(max_real_time='2.0s'),
                environ=dict(ENV='xxx'),
            )

            assert s.name == 'name_233'
            assert s.identification == Identification.loads('nobody')
            assert s.resources == ResourceLimit.loads({'max_real_time': '2.0s'})
            assert s.environ == {'V': '233', 'ENV': 'xxx'}
            assert repr(s.commands_getter(workdir='.')) == "<CommandCollection commands: 4>"
            assert repr(s.infos_getter(workdir='.')) == "<SectionInfoMapping keys: " \
                                                        "('base64', 'local', 'static', 'tag', 'value')>"
            assert repr(s.inputs_getter(workdir='.')) == "<FileInputCollection inputs: 1>"
            assert repr(s.outputs_getter(workdir='.')) == "<FileOutputCollection outputs: 4>"

    def test_section_invalid(self):
        with tempfile.TemporaryDirectory() as scriptdir, \
                FilePool() as pool:
            with codecs.open(os.path.join(scriptdir, 'README.md'), 'w') as of:
                of.write(_COMPLEX_TEXT)
            with pytest.raises(KeyError):
                _SECTION_1_TEMPLATE(
                    workdir=os.curdir,
                    scriptdir=scriptdir,
                    pool=pool,
                    identification='nobody',
                    resources=dict(max_real_time='2.0s'),
                    environ=dict(ENV='xxx'),
                )

    def test_section_call(self):
        with tempfile.TemporaryDirectory() as scriptdir, \
                FilePool() as pool:
            with codecs.open(os.path.join(scriptdir, 'README.md'), 'w') as of:
                of.write(_COMPLEX_TEXT)
            s = _SECTION_1_TEMPLATE(
                scriptdir=scriptdir,
                pool=pool,
                identification='nobody',
                resources=dict(max_real_time='2.0s'),
                environ=dict(ENV='xxx'),
            )
            _success, _results, _infos = s()

            assert _success
            assert len(_results) == 4
            assert _results[0].ok
            assert _results[1].ok
            assert _results[2].ok
            assert _results[3].ok
            assert _infos == {'static': 'this is v : 233', 'value': 233,
                              'local': 'I have a dream that one day, down in Alabama, with its vicious racists, \n'
                                       'with its governor having his lips dripping with the words of "interposition"'
                                       ' and "nullification"\n -- one day right there in Alabama little black boys'
                                       ' and black girls will be able to join \n hands with little white boys and'
                                       ' white girls as sisters and brothers.',
                              'tag': 'I have a dream that one day, down in Alabama, with its vicious racists,'
                                     ' \nwith its governor having his lips dripping with the words of "interposition"'
                                     ' and "nullification"\n -- one day right there in Alabama little black boys and'
                                     ' black girls will be able to join \n hands with little white boys and white'
                                     ' girls as sisters and brothers.',
                              'base64': 'SSBoYXZlIGEgZHJlYW0gdGhhdCBvbmUgZGF5LCBkb3duIGluIEFsYWJhbWEsIHdpdGggaXR'
                                        'zIHZp\nY2lvdXMgcmFjaXN0cywgCndpdGggaXRzIGdvdmVybm9yIGhhdmluZyBoaXMgbGlw'
                                        'cyBkcmlwcGlu\nZyB3aXRoIHRoZSB3b3JkcyBvZiAiaW50ZXJwb3NpdGlvbiIgYW5kICJud'
                                        'WxsaWZpY2F0aW9uIgog\nLS0gb25lIGRheSByaWdodCB0aGVyZSBpbiBBbGFiYW1hIGxpdH'
                                        'RsZSBibGFjayBib3lzIGFuZCBi\nbGFjayBnaXJscyB3aWxsIGJlIGFibGUgdG8gam9pbiA'
                                        'KIGhhbmRzIHdpdGggbGl0dGxlIHdoaXRl\nIGJveXMgYW5kIHdoaXRlIGdpcmxzIGFzIHNp'
                                        'c3RlcnMgYW5kIGJyb3RoZXJzLg==\n'}

            with codecs.open(os.path.join(scriptdir, 'f1.txt'), 'r') as tf:
                assert tf.read().rstrip() == '233 233'
            with codecs.open(os.path.join(scriptdir, 'f2.txt'), 'r') as tf:
                assert tf.read().rstrip() == 'xxx 233'

    def test_section_fail(self):
        with tempfile.TemporaryDirectory() as scriptdir, \
                FilePool() as pool:
            with codecs.open(os.path.join(scriptdir, 'README.md'), 'w') as of:
                of.write(_COMPLEX_TEXT)
            s = _SECTION_FAILED_TEMPLATE(
                scriptdir=scriptdir,
                pool=pool,
                identification='nobody',
                resources=dict(max_real_time='2.0s'),
                environ=dict(ENV='xxx'),
            )
            _success, _results, _infos = s()

            assert not _success
            assert len(_results) == 3
            assert _results[0].ok
            assert _results[1].ok
            assert not _results[2].ok
            assert _infos == {
                'static': 'this is v : 233', 'value': 233,
                'local_1': '233 233\n', 'local_2': 'xxx 233\n'
            }


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
