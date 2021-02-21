from string import Template
from textwrap import shorten as _shorten
from typing import Optional, Mapping


def env_template(template: str, environ: Optional[Mapping[str, str]] = None) -> str:
    return Template(template).substitute(**(environ or {}))


def truncate(text: str, width: int = 70, tail_length: int = 0, show_length: bool = False):
    text = str(text)

    if show_length:
        omission = ' ..({length} chars).. '.format(length=len(text))
    else:
        omission = ' ... '
    if tail_length:
        omission += text[len(text) - tail_length:]

    return _shorten(text, width=width, placeholder=omission)
