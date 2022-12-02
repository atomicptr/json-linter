""" Check if JSON keys are sorted """
from typing import Optional, Union

from json_linter.config import LinterConfig


def rule_keys_are_sorted(
    data: Union[dict, list],
    _config: LinterConfig
) -> (bool, Optional[str]):
    """ Check if JSON keys are sorted """
    return _are_keys_sorted(data), None


def _are_keys_sorted(obj) -> bool:
    keys = []

    if isinstance(obj, list):
        return all(map(_are_keys_sorted, obj))

    if not isinstance(obj, dict):
        return True

    for key in obj.keys():
        value = obj[key]

        keys.append(key)

        if isinstance(value, dict) and not _are_keys_sorted(value):
            return False

        if isinstance(value, list) and not all(map(_are_keys_sorted, value)):
            return False
    return sorted(keys) == keys
