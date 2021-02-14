import os
import time
from threading import Thread

import pytest

from pji.control import interactive_process


@pytest.mark.unittest
class TestControlProcessInteractive:
    def test_interactive_process_simple(self):
        _before_start = time.time()
        with interactive_process(
                args='sh',
                environ={'ENV_TEST': '233jsdf'}
        ) as ip:
            _after_start = time.time()
            assert _before_start <= ip.start_time <= _after_start
            _output = []

            def _ip_loader():
                for _rel_time, _tag, _line in ip.output_yield:
                    _output.append(_line)

            ip_loader_thread = Thread(target=_ip_loader)
            ip_loader_thread.start()

            ip.print_stdin(bytes('echo 233', 'utf8'))
            time.sleep(0.2)
            assert _output == [b'233']

            time.sleep(1.0)
            assert _output == [b'233']
            ip.print_stdin(bytes('echo ${ENV_TEST}', 'utf8'))
            time.sleep(0.2)
            assert _output == [b'233', b'233jsdf']

            ip.close_stdin()
            ip.join()

            _result = ip.result
            assert _result is not None
            assert _result.exitcode == 0
            assert _result.signal_code == 0


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
