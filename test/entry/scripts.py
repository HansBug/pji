DEMO_B64_SCRIPT = """
global:
  environ:
    PATH: /root:${PATH}
    INPUT: 2 3
  use_sys_env:
    - PATH
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
          - args: 'true'
"""

DEMO_B64_LINK_SCRIPT = """
global:
  environ:
    PATH: /root:${PATH}
    INPUT: 2 3
  use_sys_env:
    - PATH
tasks:
  run_python:
    sections:
      - name: get_test_info
        inputs:
          - "link:test_script.py:test_script.py"
        outputs:
          - "tag:wc_result.txt:wc"
          - "tag:input_result.txt:input"
        infos:
          wc: "tag:wc"
          input: "tag:input"
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
          - args: 'true'
"""

DEMO_B64_BEFORE_SCRIPT = """
global:
  environ:
    PATH: /root:${PATH}
    INPUT: 2 3 ${INPUT}
  use_sys_env:
    - PATH
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
          - args: 'true'
"""

DEMO_B64_FAIL_SCRIPT = """
global:
  environ:
    PATH: /root:${PATH}
    INPUT: 2 3
  use_sys_env:
    - PATH
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
          - args: 'false'
"""

DEMO_B64_TEST_SCRIPT_PY = """
import base64

if __name__ == '__main__':
    _line = base64.b64decode(input()).decode()
    print(sum([int(item.strip()) for item in _line.split(' ') if item.strip()]))

"""
