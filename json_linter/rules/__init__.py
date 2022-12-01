""" Linter rules """
from typing import List, Callable, Optional, Tuple

from json_linter.config import LinterConfig
from json_linter.utils import get_modules_next_to_file

Rule = Callable[[str, LinterConfig], Tuple[bool, Optional[str]]]


def get_all_rules() -> List[Rule]:
    """ Get all rules """
    rules = []

    modules = get_modules_next_to_file(__file__, __package__)

    for module in modules:
        for attr in dir(module):
            if attr.startswith("rule_"):
                rule = getattr(module, attr)
                rules.append(rule)
    return rules
