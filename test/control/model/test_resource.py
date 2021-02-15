import os

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


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
