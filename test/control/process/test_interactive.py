import os
import time
from threading import Thread

import pytest

from pji.control import interactive_process, ResourceLimit, InteractiveProcess


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestControlProcessInteractive:
    def test_interactive_process_simple(self):
        _before_start = time.time()
        with interactive_process(
                args="sh -c 'echo 233 && sleep 2 && echo 2334'",
        ) as ip:
            _after_start = time.time()
            assert _before_start <= ip.start_time <= _after_start
            _output = []

            def _ip_loader():
                for _rel_time, _tag, _line in ip.output_yield:
                    _output.append(_line)

            ip_loader_thread = Thread(target=_ip_loader)
            ip_loader_thread.start()

            time.sleep(0.5)
            assert _output == [b'233']

            time.sleep(2)
            assert _output == [b'233', b'2334']

            ip.close_stdin()
            ip.join()

            _result = ip.process_result
            assert _result is not None
            assert _result.exitcode == 0
            assert _result.signal_code == 0

    def test_interactive_process_with_env(self):
        _before_start = time.time()
        with interactive_process(
                args="sh -c 'echo 233 && sleep 2 && echo ${ENV_TEST}'",
                environ={'ENV_TEST': '2334'},
        ) as ip:
            _after_start = time.time()
            assert _before_start <= ip.start_time <= _after_start
            _output = []

            def _ip_loader():
                for _rel_time, _tag, _line in ip.output_yield:
                    _output.append(_line)

            ip_loader_thread = Thread(target=_ip_loader)
            ip_loader_thread.start()

            time.sleep(0.5)
            assert _output == [b'233']

            time.sleep(2)
            assert _output == [b'233', b'2334']

            ip.close_stdin()
            ip.join()

            _result = ip.process_result
            assert _result is not None
            assert _result.exitcode == 0
            assert _result.signal_code == 0

    def test_interactive_process_with_input(self):
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

            assert ip.process_result is None

            ip.close_stdin()
            ip.join()

            _result = ip.process_result
            assert _result is not None
            assert _result.exitcode == 0
            assert _result.signal_code == 0

    def test_interactive_process_rtle(self):
        _before_start = time.time()
        with interactive_process(
                args='sh',
                environ={'ENV_TEST': '233jsdf'},
                resources=ResourceLimit(
                    max_real_time='2s',
                )
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

            time.sleep(2.0)
            assert _output == [b'233']
            ip.print_stdin(bytes('echo ${ENV_TEST}', 'utf8'))
            time.sleep(0.2)
            assert _output == [b'233']

            ip.close_stdin()
            ip.join()

            _result = ip.process_result
            assert _result is not None
            assert _result.exitcode == 0
            assert _result.signal_code == 9

    def test_interactive_process_rtle_pass(self):
        _before_start = time.time()
        with interactive_process(
                args='sh',
                environ={'ENV_TEST': '233jsdf'},
                resources=ResourceLimit(
                    max_real_time='4s',
                )
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

            time.sleep(2.0)
            assert _output == [b'233']
            ip.print_stdin(bytes('echo ${ENV_TEST}', 'utf8'))
            time.sleep(0.2)
            assert _output == [b'233', b'233jsdf']

            assert ip.process_result is None

            ip.close_stdin()
            ip.join()

            _result = ip.process_result
            assert _result is not None
            assert _result.exitcode == 0
            assert _result.signal_code == 0

    def test_interactive_process_direct_close(self):
        with interactive_process(
                args="sh",
        ) as ip:
            assert isinstance(ip, InteractiveProcess)
            ip.close_stdin()
            _outputs = list(ip.output_yield)

        assert len(_outputs) == 0
        _result = ip.process_result
        assert _result.ok

    def test_interactive_process_wtf(self):
        with pytest.raises(EnvironmentError):
            with interactive_process(
                    args="what_the_fuck -c 'echo 233 && sleep 2 && echo 2334'",
            ):
                pytest.fail('Should not reach here')


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
