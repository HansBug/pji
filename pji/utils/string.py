from string import Template
from textwrap import shorten as _shorten
from typing import Optional, Mapping


def env_template(template: str, environ: Optional[Mapping[str, str]] = None, safe: bool = False) -> str:
    _template = Template(template)
    _func = _template.safe_substitute if safe else _template.substitute
    return _func(**(environ or {}))


def truncate(text: str, width: int = 70, tail_length: int = 0, show_length: bool = False):
    text = str(text)

    if show_length:
        omission = ' ..({length} chars).. '.format(length=len(text))
    else:
        omission = ' ... '
    if tail_length:
        omission += text[len(text) - tail_length:]

    return _shorten(text, width=width, placeholder=omission)
