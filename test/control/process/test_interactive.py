import os
import time
from threading import Thread

import pytest

from pji.control import interactive_process, ResourceLimit, InteractiveProcess, RunResultStatus


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestControlProcessInteractive:
    def test_interactive_process_simple(self):
        _before_start = time.time()
        with interactive_process(
                args="echo 233 && sleep 2 && echo 2334",
                shell=True,
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

            time.sleep(3)
            assert _output == [b'233', b'2334']

            ip.close_stdin()
            ip.join()

            _result = ip.result.result
            assert _result is not None
            assert _result.exitcode == 0
            assert _result.signal_code == 0

    def test_interactive_process_with_env(self):
        _before_start = time.time()
        with interactive_process(
                args="echo 233 && sleep 2 && echo ${ENV_TEST}",
                shell=True,
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

            time.sleep(3)
            assert _output == [b'233', b'2334']

            ip.close_stdin()
            ip.join()

            _result = ip.result.result
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

            assert ip.result.result is None
            assert ip.status == RunResultStatus.NOT_COMPLETED
            assert not ip.ok
            assert not ip.completed

            ip.close_stdin()
            ip.join()

            _result = ip.result.result
            assert ip.ok
            assert ip.completed
            assert ip.status == RunResultStatus.SUCCESS
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
            with pytest.raises(BrokenPipeError):
                ip.print_stdin(bytes('echo ${ENV_TEST}', 'utf8'))
            time.sleep(0.2)
            assert _output == [b'233']

            with pytest.raises(BrokenPipeError):
                ip.print_stdin(bytes('echo ${ENV_TEST}', 'utf8'))

            with pytest.raises(BrokenPipeError):
                ip.print_stdin(bytes('echo ${ENV_TEST}', 'utf8'))

            ip.close_stdin()
            ip.join()

            _result = ip.result.result
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

            assert ip.result.result is None
            assert ip.result.status == RunResultStatus.NOT_COMPLETED
            assert not ip.ok
            assert not ip.completed

            ip.close_stdin()
            ip.join()

            _result = ip.result.result
            assert ip.ok
            assert ip.completed
            assert ip.status == RunResultStatus.SUCCESS
            assert _result.ok
            assert _result is not None
            assert _result.exitcode == 0
            assert _result.signal_code == 0

    @pytest.mark.timeout(5.0)
    def test_interactive_process_direct_close_1(self):
        with interactive_process(
                args="sh",
        ) as ip:
            assert isinstance(ip, InteractiveProcess)

            ip.print_stdin(b'echo 233')
            _, _tag, _line = next(ip.output_yield)
            assert _tag == 'stdout'
            assert _line.rstrip(b'\r\n') == b'233'

            ip.print_stdin(b'echo 2334')
            _, _tag, _line = next(ip.output_yield)
            assert _tag == 'stdout'
            assert _line.rstrip(b'\r\n') == b'2334'

        _result = ip.result.result
        assert _result.ok

    @pytest.mark.timeout(5.0)
    def test_interactive_process_direct_close_2(self):
        with interactive_process(
                args="sh",
        ) as ip:
            assert isinstance(ip, InteractiveProcess)

            ip.print_stdin(b'echo 233')
            _, _tag, _line = next(ip.output_yield)
            assert _tag == 'stdout'
            assert _line.rstrip(b'\r\n') == b'233'

            ip.print_stdin(b'echo 2334')
            _, _tag, _line = next(ip.output_yield)
            assert _tag == 'stdout'
            assert _line.rstrip(b'\r\n') == b'2334'

            ip.close_stdin()

        _result = ip.result.result
        assert _result.ok

    def test_interactive_process_wtf(self):
        with pytest.raises(EnvironmentError):
            with interactive_process(
                    args="what_the_fuck -c 'echo 233 && sleep 2 && echo 2334'",
            ):
                pytest.fail('Should not reach here')


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
