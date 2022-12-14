""" Sorts JSON file by keys """
import json
from typing import Union, List, Dict, Tuple

from json_linter.config import LinterConfig
from json_linter.utils import natural_keys


def fix_sorted_keys(data: str, _config: LinterConfig) -> str:
    """ Fix json file to be sorted by key """
    json_data = json.loads(data)
    json_data = _sort_dict(json_data)
    return json.dumps(json_data)


def _sort_dict(item: Union[List, Dict]) -> Union[List, Dict]:
    def _sort(tpl: Tuple):
        key, value = tpl
        return natural_keys(key), value

    if isinstance(item, list):
        return list(map(_sort_dict, item))
    if isinstance(item, dict):
        return {k: _sort_dict(v) for k, v in sorted(item.items(), key=_sort)}
    return item
