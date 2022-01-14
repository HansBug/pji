import resource
from multiprocessing import Manager, Process

import pytest

from pji.control.model import ResourceLimit


@pytest.mark.unittest
class TestControlModelResource:
    def test_properties(self):
        rl = ResourceLimit(
            max_stack=1,
            max_memory=2,
            max_cpu_time=3,
            max_real_time=4,
            max_output_size=5,
            max_process_number=6,
        )

        assert rl.max_stack == 1
        assert rl.max_memory == 2
        assert rl.max_cpu_time == 3
        assert rl.max_real_time == 4
        assert rl.max_output_size == 5
        assert rl.max_process_number == 6

    def test_load_from_json(self):
        rl = ResourceLimit.load_from_json(dict(
            max_stack=1,
            max_memory=2,
            max_cpu_time=3,
            max_real_time=4,
            max_output_size=5,
            max_process_number=6,
        ))

        assert rl.max_stack == 1
        assert rl.max_memory == 2
        assert rl.max_cpu_time == 3
        assert rl.max_real_time == 4
        assert rl.max_output_size == 5
        assert rl.max_process_number == 6

    def test_to_json(self):
        rl = ResourceLimit(
            max_stack=1,
            max_memory=2,
            max_cpu_time=3,
            max_real_time=4,
            max_output_size=5,
            max_process_number=6,
        )

        assert rl.json == dict(
            max_stack=1,
            max_memory=2,
            max_cpu_time=3,
            max_real_time=4,
            max_output_size=5,
            max_process_number=6,
        )

    def test_repr(self):
        assert repr(ResourceLimit()) == '<ResourceLimit>'
        assert repr(ResourceLimit(max_real_time=2.3)) == '<ResourceLimit real time: 2.300s>'
        assert repr(ResourceLimit(
            max_stack=1,
            max_memory=2,
            max_cpu_time=3,
            max_real_time=4,
            max_output_size=5,
            max_process_number=6,
        )) == '<ResourceLimit cpu time: 3.000s, real time: 4.000s, memory: 2.0 Byte, ' \
              'stack: 1.0 Byte, process: 6, output size: 5.0 Byte>'

    def test_eq(self):
        rl = ResourceLimit(
            max_stack=1,
            max_memory=2,
            max_cpu_time=3,
            max_real_time=4,
            max_output_size=5,
            max_process_number=6,
        )
        assert rl == rl

        assert ResourceLimit.merge(
            ResourceLimit(max_memory=2),
            ResourceLimit(max_cpu_time=3),
        ) == ResourceLimit(
            max_memory=2,
            max_cpu_time=3,
        )

        assert not (rl == 1)

    def test_hash(self):
        h = {
            ResourceLimit(
                max_memory=2,
                max_cpu_time=3,
            ): 1,
            ResourceLimit(
                max_stack=1,
                max_memory=2,
                max_cpu_time=3,
                max_real_time=4,
                max_output_size=5,
                max_process_number=6,
            ): 2,
        }

        assert h[ResourceLimit(
            max_memory=2,
            max_cpu_time=3,
        )] == 1
        assert h[ResourceLimit(
            max_stack=1,
            max_memory=2,
            max_cpu_time=3,
            max_real_time=4,
            max_output_size=5,
            max_process_number=6,
        )] == 2

    def test_merge(self):
        assert ResourceLimit.merge(
            ResourceLimit(max_memory=2),
            ResourceLimit(max_cpu_time=3),
        ).json == dict(
            max_output_size=None,
            max_real_time=None,
            max_stack=None,
            max_process_number=None,
            max_memory=2,
            max_cpu_time=3,
        )

        assert ResourceLimit.merge(ResourceLimit(
            max_stack=1,
            max_memory=2,
            max_cpu_time=3,
            max_real_time=4,
            max_output_size=5,
            max_process_number=6,
        ), ResourceLimit(
            max_stack=6,
            max_memory=5,
            max_cpu_time=4,
            max_real_time=3,
            max_output_size=2,
            max_process_number=1,
        )).json == dict(
            max_stack=1,
            max_memory=2,
            max_cpu_time=3,
            max_real_time=3,
            max_output_size=2,
            max_process_number=1,
        )

    def test_apply_1(self):
        with Manager() as manager:
            _result = manager.dict(dict(
                max_cpu_time=None,
                max_memory=None,
                max_stack=None,
                max_output_size=None,
                max_process_number=None,
            ))

            # noinspection PyTypeChecker,DuplicatedCode
            def _get_user_and_group():
                rl = ResourceLimit(
                    max_cpu_time='5s',
                    max_memory='512mb',
                    max_stack='1G',
                    max_output_size='64m',
                    max_process_number=3,
                )
                rl.apply()
                _result['max_cpu_time'] = resource.getrlimit(resource.RLIMIT_CPU)
                _result['max_memory'] = resource.getrlimit(resource.RLIMIT_AS)
                _result['max_stack'] = resource.getrlimit(resource.RLIMIT_STACK)
                _result['max_output_size'] = resource.getrlimit(resource.RLIMIT_FSIZE)
                _result['max_process_number'] = resource.getrlimit(resource.RLIMIT_NPROC)

            p = Process(target=_get_user_and_group)
            p.start()
            p.join()

            _result = dict(_result)
            assert _result == dict(
                max_cpu_time=(6, 6),
                max_memory=(780435456, 780435456),
                max_stack=(1000000000, 1000000000),
                max_output_size=(64000000, 64000000),
                max_process_number=(3, 3),
            )

    def test_apply_2(self):
        with Manager() as manager:
            _result = manager.dict(dict(
                max_cpu_time=None,
                max_memory=None,
                max_stack=None,
                max_output_size=None,
            ))

            # noinspection PyTypeChecker,DuplicatedCode
            def _get_user_and_group():
                rl = ResourceLimit()
                rl.apply()
                _result['max_cpu_time'] = resource.getrlimit(resource.RLIMIT_CPU)
                _result['max_memory'] = resource.getrlimit(resource.RLIMIT_AS)
                _result['max_stack'] = resource.getrlimit(resource.RLIMIT_STACK)
                _result['max_output_size'] = resource.getrlimit(resource.RLIMIT_FSIZE)

            p = Process(target=_get_user_and_group)
            p.start()
            p.join()

            _result = dict(_result)
            assert _result == dict(
                max_cpu_time=(-1, -1),
                max_memory=(-1, -1),
                max_stack=(-1, -1),
                max_output_size=(-1, -1),
            )
