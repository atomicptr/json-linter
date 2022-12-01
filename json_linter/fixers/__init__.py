""" Fix issues in JSON files """
from typing import List, Callable

from json_linter.config import LinterConfig
from json_linter.utils import get_modules_next_to_file

Fixer = Callable[[str, LinterConfig], str]


def get_all_fixers() -> List[Fixer]:
    """ Get all fixers """
    fixers = []

    modules = get_modules_next_to_file(__file__, __package__)

    for module in modules:
        for attr in dir(module):
            if attr.startswith("fix_"):
                rule = getattr(module, attr)
                fixers.append(rule)
    return fixers
