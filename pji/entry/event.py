import codecs
import os

from ..service import DispatchTemplate
from ..utils import auto_load_json

_DEFAULT_FILENAME = 'pscript.yml'


def _load_dispatch_template(filename: str) -> DispatchTemplate:
    with codecs.open(filename, 'r') as file:
        _json = auto_load_json(file)

    return DispatchTemplate.loads(_json)
