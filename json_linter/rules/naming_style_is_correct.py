""" Check if keys in JSON file match with the configured naming style """
from typing import Optional, Union, Pattern
import re

from json_linter.config import LinterConfig, NamingStyle

_KEBAB_CASE_REGEX = r"^([a-z\-]+)$"
_SNAKE_CASE_REGEX = r"^([a-z\_]+)$"
_CAMEL_CASE_REGEX = r"^([a-zA-Z]+)$"


def rule_naming_style_is_correct(
    data: Union[dict, list],
    config: LinterConfig
) -> (bool, Optional[str]):
    """ Check if naming style is correct """
    if config.naming_style is None:
        return True, None

    pattern = None

    if config.naming_style == NamingStyle.CAMEL_CASE:
        pattern = _CAMEL_CASE_REGEX
    elif config.naming_style == NamingStyle.SNAKE_CASE:
        pattern = _SNAKE_CASE_REGEX
    elif config.naming_style == NamingStyle.KEBAB_CASE:
        pattern = _KEBAB_CASE_REGEX

    if pattern is None:
        return True, None

    pattern = re.compile(pattern)

    return _are_keys_valid(pattern, data), None


def _are_keys_valid(pattern: Pattern, obj: Union[dict, list]) -> bool:
    if isinstance(obj, list):
        return all(map(lambda elem: _are_keys_valid(pattern, elem), obj))
    if not isinstance(obj, dict):
        return True
    for key in obj.keys():
        if not pattern.match(key):
            return False
        value = obj[key]

        if isinstance(value, (dict, list)):
            child_valid = _are_keys_valid(pattern, value)

            if not child_valid:
                return False
    return True
