""" Check if JSON keys are sorted """
import json
from typing import Optional

from json_linter.config import LinterConfig


def rule_keys_are_sorted(
    data: str,
    _config: LinterConfig
) -> (bool, Optional[str]):
    """ Check if JSON keys are sorted """
    obj = json.loads(data)
    return _are_keys_sorted(obj), None


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
