# pji

[![PyPI](https://img.shields.io/pypi/v/pji)](https://pypi.org/project/pji/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pji)](https://pypi.org/project/pji/)
![Loc](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/HansBug/fe11c430393128dda3a998423a95ed57/raw/loc.json)
![Comments](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/HansBug/fe11c430393128dda3a998423a95ed57/raw/comments.json)

[![Docs Deploy](https://github.com/HansBug/pji/workflows/Docs%20Deploy/badge.svg)](https://github.com/HansBug/pji/actions?query=workflow%3A%22Docs+Deploy%22)
[![Code Test](https://github.com/HansBug/pji/workflows/Code%20Test/badge.svg)](https://github.com/HansBug/pji/actions?query=workflow%3A%22Code+Test%22)
[![Badge Creation](https://github.com/HansBug/pji/workflows/Badge%20Creation/badge.svg)](https://github.com/HansBug/pji/actions?query=workflow%3A%22Badge+Creation%22)
[![Package Release](https://github.com/HansBug/pji/workflows/Package%20Release/badge.svg)](https://github.com/HansBug/pji/actions?query=workflow%3A%22Package+Release%22)
[![codecov](https://codecov.io/gh/HansBug/pji/branch/main/graph/badge.svg?token=XJVDP4EFAT)](https://codecov.io/gh/HansBug/pji)

[![GitHub stars](https://img.shields.io/github/stars/HansBug/pji)](https://github.com/HansBug/pji/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/HansBug/pji)](https://github.com/HansBug/pji/network)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/HansBug/pji)
[![GitHub issues](https://img.shields.io/github/issues/HansBug/pji)](https://github.com/HansBug/pji/issues)
[![GitHub pulls](https://img.shields.io/github/issues-pr/HansBug/pji)](https://github.com/HansBug/pji/pulls)
[![Contributors](https://img.shields.io/github/contributors/HansBug/pji)](https://github.com/HansBug/pji/graphs/contributors)
[![GitHub license](https://img.shields.io/github/license/HansBug/pji)](https://github.com/HansBug/pji/blob/master/LICENSE)


An easy-to-use python interaction for judgement.

一款新型的评测机内核，支持了一些新功能和特性，在第一版本（`pyjudge`）基础上进行了较大的扩展。

## 安装

源代码安装

```shell
git clone git@gitlab.buaaoo.top:oo_system/judge/pji.git
cd pji
pip install .
```

卸载

```shell
pip uninstall pji
```

## 开始使用

开始使用前请务必注意：

* pji依赖于pji包（指的是OO课程组内的那个，不是pypi上的`pySystem`），如果没有pypi平台支持的话，需要先手动安装版本合适的pji
* pji的一系列功能，包括降权、限制资源、系统交互等，都是**需要root权限**的，请在使用时务必注意
* pji由于功能限制，故**只支持linux系统环境下使用**，且目前只在ubuntu上做过测试，请在使用时务必注意

### 命令行使用

pji采用基于配置文件的使用方式，命令行帮助信息如下

```shell
pji -h
```

内容如下

```
Usage: pji [OPTIONS]

Options:
  -v, --version             Show package's version information.
  -s, --script FILE         Path of pji script.  [default: pscript.yml]
  -t, --task TEXT           Task going to be executed.  [default: main]
  -e, --environ TEXT        Environment variables (loaded before global
                            config).

  -E, --environ_after TEXT  Environment variables (loaded after global
                            config).

  -h, --help                Show this message and exit.

```

一个简单的使用示例，设有配置文件`test_dispatch.yml`

```yml
global:
  environ:
    PATH: /root:${PATH}
    INPUT: 2 3
  use_sys_env:
    - PATH
    - LC_ALL
    - LANG
tasks:
  run_python:
    sections:
      - name: get_test_info
        inputs:
          - "copy:test_script.py:test_script.py"
        outputs:
          - "tag:wc_result.txt:wc"
          - "tag:input_result.txt:input"
        infos:
          wc: "tag:wc"
          input: "tag:input"
        info_dump: "test_info.txt"
        commands:
          - args: "cat test_script.py | wc -l"
            stdout: wc_result.txt
          - args: "echo ${INPUT}"
            stdout: input_result.txt
      - name: generate_base64
        outputs:
          - "tag:base64.txt:b64"
        infos:
          b64: "tag:b64"
        commands:
          - args: "echo ${INPUT} | base64"
            stdout: base64.txt
      - name: run_result
        identification: nobody
        inputs:
          - "copy:test_script.py:test_script.py:r--:nobody"
          - "tag:b64:base64.txt:r--:nobody"
        outputs:
          - "tag:result.txt:result"
          - "copy:result.txt:test_result.txt"
        infos:
          result: "tag:result"
        commands:
          - args: "cat base64.txt | python test_script.py"
            stdout: result.txt
          - 'true'
```

脚本文件`test_script.py`

```python
import base64

if __name__ == '__main__':
    _line = base64.b64decode(input()).decode()
    print(sum([int(item.strip()) for item in _line.split(' ') if item.strip()]))

```

这两者均位于目录`/root/123`下，故可以运行

```shell
pji -s /root/123/test_dispatch.yml -t run_python
```

则有输出

```
Section 'get_test_info' start ...
Coping file from '/root/123/test_script.py' to '/tmp/tmp6rsk6t2o/test_script.py' ... COMPLETE
Running 'cat test_script.py | wc -l' ... SUCCESS, time: 0.002s / 0.002s, memory: 18.875 MiB
Running 'echo ${INPUT}' ... SUCCESS, time: 0.004s / 0.003s, memory: 19.125 MiB
Saving file from '/tmp/tmp6rsk6t2o/wc_result.txt' to tag 'wc' ... COMPLETE
Saving file from '/tmp/tmp6rsk6t2o/input_result.txt' to tag 'input' ... COMPLETE
Collecting result information ... COMPLETE
Dumping result information to '/root/123/test_info.txt' ... COMPLETE
Section 'get_test_info' execute completed!

Section 'generate_base64' start ...
Running 'echo ${INPUT} | base64' ... SUCCESS, time: 0.003s / 0.002s, memory: 19.15625 MiB
Saving file from '/tmp/tmp_n5ftp5d/base64.txt' to tag 'b64' ... COMPLETE
Collecting result information ... COMPLETE
Section 'generate_base64' execute completed!

Section 'run_result' start ...
Coping file from '/root/123/test_script.py' to '/tmp/tmphcbmt0j9/test_script.py' ... COMPLETE
Loading tag 'b64' to '/tmp/tmphcbmt0j9/base64.txt' ... COMPLETE
Running 'cat base64.txt | python test_script.py' ... SUCCESS, time: 0.025s / 0.030s, memory: 19.16796875 MiB
Running 'true' ... SUCCESS, time: 0.000s / 0.001s, memory: 19.18359375 MiB
Saving file from '/tmp/tmphcbmt0j9/result.txt' to tag 'result' ... COMPLETE
Coping file from '/tmp/tmphcbmt0j9/result.txt' to '/root/123/test_result.txt' ... COMPLETE
Collecting result information ... COMPLETE
Section 'run_result' execute completed!

Task success.

```

以及回传的文件`/root/123/result.txt`

```
5
```

此外，当执行命令行

```shell
pji -s /root/123/test_dispatch.yml -t run_python -E "INPUT=1 2 3 4 5 6 7"
```

则有`/root/123/result.txt`

```
28
```

以及如果需要导出完整的运行信息，可以执行命令行

```shell
pji -s /root/123/test_dispatch.yml -t run_python -E "INPUT=1 2 3 4 5 6 7" -i test_info.json
```

则会额外有文件`test_info.json`

```json
{
    "ok": true,
    "sections": [
        {
            "commands": [
                {
                    "completed": true,
                    "limit": {
                        "max_cpu_time": null,
                        "max_memory": null,
                        "max_output_size": null,
                        "max_process_number": null,
                        "max_real_time": null,
                        "max_stack": null
                    },
                    "ok": true,
                    "result": {
                        "cpu_time": 0.000896,
                        "exitcode": 0,
                        "max_memory": 19709952.0,
                        "real_time": 0.002176523208618164,
                        "signal": null
                    },
                    "status": "SUCCESS"
                },
                {
                    "completed": true,
                    "limit": {
                        "max_cpu_time": null,
                        "max_memory": null,
                        "max_output_size": null,
                        "max_process_number": null,
                        "max_real_time": null,
                        "max_stack": null
                    },
                    "ok": true,
                    "result": {
                        "cpu_time": 0.002518,
                        "exitcode": 0,
                        "max_memory": 19881984.0,
                        "real_time": 0.0010895729064941406,
                        "signal": null
                    },
                    "status": "SUCCESS"
                }
            ],
            "information": {
                "input": "1 2 3 4 5 6 7\n",
                "wc": "5\n"
            },
            "name": "get_test_info",
            "ok": true
        },
        {
            "commands": [
                {
                    "completed": true,
                    "limit": {
                        "max_cpu_time": null,
                        "max_memory": null,
                        "max_output_size": null,
                        "max_process_number": null,
                        "max_real_time": null,
                        "max_stack": null
                    },
                    "ok": true,
                    "result": {
                        "cpu_time": 0.002568,
                        "exitcode": 0,
                        "max_memory": 19922944.0,
                        "real_time": 0.0018069744110107422,
                        "signal": null
                    },
                    "status": "SUCCESS"
                }
            ],
            "information": {
                "b64": "MSAyIDMgNCA1IDYgNwo=\n"
            },
            "name": "generate_base64",
            "ok": true
        },
        {
            "commands": [
                {
                    "completed": true,
                    "limit": {
                        "max_cpu_time": null,
                        "max_memory": null,
                        "max_output_size": null,
                        "max_process_number": null,
                        "max_real_time": null,
                        "max_stack": null
                    },
                    "ok": true,
                    "result": {
                        "cpu_time": 0.023656999999999997,
                        "exitcode": 0,
                        "max_memory": 19947520.0,
                        "real_time": 0.027228593826293945,
                        "signal": null
                    },
                    "status": "SUCCESS"
                },
                {
                    "completed": true,
                    "limit": {
                        "max_cpu_time": null,
                        "max_memory": null,
                        "max_output_size": null,
                        "max_process_number": null,
                        "max_real_time": null,
                        "max_stack": null
                    },
                    "ok": true,
                    "result": {
                        "cpu_time": 0.001723,
                        "exitcode": 0,
                        "max_memory": 19955712.0,
                        "real_time": 0.0009958744049072266,
                        "signal": null
                    },
                    "status": "SUCCESS"
                }
            ],
            "information": {
                "result": "28\n"
            },
            "name": "run_result",
            "ok": true
        }
    ]
}
```



### 脚本使用

实际上pji也支持用程序的方式进行如上的调用。

例如对于上述两个文件，我们可以编写这样的程序

```python
import codecs

from pji.entry import load_pji_script

if __name__ == '__main__':
    _script = load_pji_script('/root/123/test_dispatch.yml')
    _success, _result = _script('run_python')

    print(_success)
    print(_result)

    with codecs.open('/root/123/test_result.txt', 'r') as rf:
        print(rf.read())

```

输出结果为

```
True
[('get_test_info', (True, [<RunResult status: SUCCESS>, <RunResult status: SUCCESS>], {'wc': '5\n', 'input': '2 3\n'})), ('generate_base64', (True, [<RunResult status: SUCCESS>], {'b64': 'MiAzCg==\n'})), ('run_result', (True, [<RunResult status: SUCCESS>, <RunResult status: SUCCESS>], {'result': '5\n'}))]
5
```

此外也有

```python
import codecs

from pji.entry import load_pji_script

if __name__ == '__main__':
    _script = load_pji_script('/root/123/test_dispatch.yml')
    _success, _result = _script('run_python', environ_after={'INPUT': '1 2 3 4 5 6 7'})

    print(_success)
    print(_result)

    with codecs.open('/root/123/test_result.txt', 'r') as rf:
        print(rf.read())

```

输出的结果为

```
True
[('get_test_info', (True, [<RunResult status: SUCCESS>, <RunResult status: SUCCESS>], {'wc': '5\n', 'input': '1 2 3 4 5 6 7\n'})), ('generate_base64', (True, [<RunResult status: SUCCESS>], {'b64': 'MSAyIDMgNCA1IDYgNwo=\n'})), ('run_result', (True, [<RunResult status: SUCCESS>, <RunResult status: SUCCESS>], {'result': '28\n'}))]
28
```

## 更多细节

（暂时先不想写了，后续再填坑吧）