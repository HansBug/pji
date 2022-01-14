import os

import mock
import pytest

from pji.control.model import Identification, ResourceLimit
from pji.service.dispatch.global_ import GlobalConfigTemplate


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestServiceDispatchGlobal:
    def test_template_simple(self):
        gt = GlobalConfigTemplate(
            identification='nobody',
            resources=dict(max_real_time='2.0s'),
            environ=dict(VAR1='2333'),
        )

        assert gt.identification == Identification.loads('nobody')
        assert gt.resources == ResourceLimit.loads(dict(max_real_time='2.0s'))
        assert gt.environ == {'VAR1': '2333'}
        assert gt.use_sys_env is False
        assert repr(gt) == "<GlobalConfigTemplate identification: " \
                           "<Identification user: nobody, group: nogroup>, " \
                           "resources: <ResourceLimit real time: 2.000s>, " \
                           "environ: {'VAR1': '2333'}, use_sys_env: False>"

    def test_template_sys_env_all(self):
        gt = GlobalConfigTemplate(
            identification='nobody',
            resources=dict(max_real_time='2.0s'),
            environ=dict(VAR1='2333'),
            use_sys_env=True,
        )
        assert gt.identification == Identification.loads('nobody')
        assert gt.resources == ResourceLimit.loads(dict(max_real_time='2.0s'))
        assert gt.environ == {'VAR1': '2333'}
        assert gt.use_sys_env is True
        assert repr(gt) == "<GlobalConfigTemplate identification: " \
                           "<Identification user: nobody, group: nogroup>, " \
                           "resources: <ResourceLimit real time: 2.000s>, " \
                           "environ: {'VAR1': '2333'}, use_sys_env: True>"

    def test_template_sys_env_parts(self):
        gt = GlobalConfigTemplate(
            identification='nobody',
            resources=dict(max_real_time='2.0s'),
            environ=dict(VAR1='2333'),
            use_sys_env=['CLASSPATH', 'PATH'],
        )
        assert gt.identification == Identification.loads('nobody')
        assert gt.resources == ResourceLimit.loads(dict(max_real_time='2.0s'))
        assert gt.environ == {'VAR1': '2333'}
        assert gt.use_sys_env == {'CLASSPATH', "PATH"}
        assert repr(gt) in [
            "<GlobalConfigTemplate identification: "
            "<Identification user: nobody, group: nogroup>, "
            "resources: <ResourceLimit real time: 2.000s>, "
            "environ: {'VAR1': '2333'}, use_sys_env: {'PATH', 'CLASSPATH'}>",
            "<GlobalConfigTemplate identification: "
            "<Identification user: nobody, group: nogroup>, "
            "resources: <ResourceLimit real time: 2.000s>, "
            "environ: {'VAR1': '2333'}, use_sys_env: {'CLASSPATH', 'PATH'}>",
        ]

    def test_template_invalid(self):
        with pytest.raises(TypeError):
            GlobalConfigTemplate(
                identification='nobody',
                resources=dict(max_real_time='2.0s'),
                environ=dict(VAR1='2333'),
                use_sys_env=233,
            )

    def test_template_call(self):
        gt = GlobalConfigTemplate(
            identification='nobody',
            resources=dict(max_real_time='2.0s'),
            environ=dict(VAR1='2333'),
        )

        g = gt()
        assert g.identification == Identification.loads('nobody')
        assert g.resources == ResourceLimit.loads(dict(max_real_time='2.0s'))
        assert g.environ == {'VAR1': '2333'}
        assert repr(g) == "<GlobalConfig identification: " \
                          "<Identification user: nobody, group: nogroup>, " \
                          "resources: <ResourceLimit real time: 2.000s>, " \
                          "environ: {'VAR1': '2333'}>"

    def test_template_call_with_all_sys_env(self):
        gt = GlobalConfigTemplate(
            identification='nobody',
            resources=dict(max_real_time='2.0s'),
            environ=dict(VAR1='2333', PATH='/1/2/3:${PATH}'),
            use_sys_env=True,
        )

        g = gt()
        assert g.identification == Identification.loads('nobody')
        assert g.resources == ResourceLimit.loads(dict(max_real_time='2.0s'))
        assert g.environ['VAR1'] == '2333'
        assert g.environ['PATH'] == '/1/2/3:' + os.environ['PATH']
        assert g.environ['PWD'] == os.path.abspath(os.curdir)

    def test_template_call_with_some_sys_env(self):
        gt = GlobalConfigTemplate(
            identification='nobody',
            resources=dict(max_real_time='2.0s'),
            environ=dict(VAR1='2333', PATH='/1/2/3:${PATH}'),
            use_sys_env=['PATH'],
        )

        g = gt()
        assert g.identification == Identification.loads('nobody')
        assert g.resources == ResourceLimit.loads(dict(max_real_time='2.0s'))
        assert g.environ == {
            'VAR1': '2333',
            'PATH': '/1/2/3:' + os.environ['PATH'],
        }

    @mock.patch.dict(os.environ, {"PATH": "/3/4/5", "PATH1": '/path/1', 'PATH233': '/path/233'})
    def test_template_all_with_before_env(self):
        gt = GlobalConfigTemplate(
            identification='nobody',
            resources=dict(max_real_time='2.0s'),
            environ=dict(VAR1='2333', PATH='${RUBY_ROOT}:${PATH}'),
            use_sys_env=['PATH*'],
        )

        g = gt(environ=dict(RUBY_ROOT='/root/ruby'))
        assert g.identification == Identification.loads('nobody')
        assert g.resources == ResourceLimit.loads(dict(max_real_time='2.0s'))
        assert g.environ == {
            'VAR1': '2333',
            'RUBY_ROOT': '/root/ruby',
            'PATH': '/root/ruby:/3/4/5',
            "PATH1": '/path/1',
            'PATH233': '/path/233'
        }

    def test_template_all_with_ext_env(self):
        gt = GlobalConfigTemplate(
            identification='nobody',
            resources=dict(max_real_time='2.0s'),
            environ=dict(VAR1='2333', PATH='${RUBY_ROOT}:${PATH}'),
            use_sys_env=['PATH'],
        )

        g = gt(environ=dict(RUBY_ROOT='/root/ruby'), environ_after=dict(PATH='/1/2/3'))
        assert g.identification == Identification.loads('nobody')
        assert g.resources == ResourceLimit.loads(dict(max_real_time='2.0s'))
        assert g.environ == {
            'VAR1': '2333',
            'RUBY_ROOT': '/root/ruby',
            'PATH': '/1/2/3',
        }

    def test_template_loads(self):
        gt = GlobalConfigTemplate(
            identification='nobody',
            resources=dict(max_real_time='2.0s'),
            environ=dict(VAR1='2333', PATH='${RUBY_ROOT}:${PATH}'),
            use_sys_env=['PATH'],
        )

        assert GlobalConfigTemplate.loads(gt) == gt
        assert GlobalConfigTemplate.loads(dict(
            identification='nobody',
            resources=dict(max_real_time='2.0s'),
            environ=dict(VAR1='2333', PATH='${RUBY_ROOT}:${PATH}'),
            use_sys_env=['PATH'],
        )).use_sys_env == {'PATH'}

        with pytest.raises(TypeError):
            GlobalConfigTemplate.loads(1223)

    def test_global_call(self):
        gt = GlobalConfigTemplate(
            identification='nobody',
            resources=dict(max_real_time='2.0s'),
            environ=dict(VAR1='2333', PATH='${RUBY_ROOT}:${PATH}'),
            use_sys_env=['PATH'],
        )

        g = gt(environ=dict(RUBY_ROOT='/root/ruby'))
        assert g() == (
            Identification.loads('nobody'),
            ResourceLimit.loads(dict(max_real_time='2.0s')),
            {
                'VAR1': '2333',
                'RUBY_ROOT': '/root/ruby',
                'PATH': '/root/ruby:' + os.environ['PATH'],
            },
        )
