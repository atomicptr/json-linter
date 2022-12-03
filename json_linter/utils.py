""" Utility functions """
import os
from importlib import import_module
from math import floor
from pathlib import Path
from types import ModuleType
from typing import List, Dict, Optional

COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_RESET = "\033[00m"


def flatten(items: List) -> List:
    """ Flatten list """
    new_list: List = []

    if not isinstance(items, list):
        return new_list

    for item in items:
        if isinstance(item, list):
            new_list.extend(flatten(item))
            continue
        new_list.append(item)
    return new_list


def get_modules_next_to_file(file: str, package: str) -> List[ModuleType]:
    """ Get all modules next to file in package """
    folder = Path(file).parent

    modules = []

    for python_file in folder.glob("*.py"):
        if python_file.name.startswith("__"):
            continue

        module_name = python_file.name[:-3]
        modules.append(import_module(f".{module_name}", package))

    return modules


def parse_var(string: str) -> (str, str):
    """ Parses a key value pair """
    items = string.split("=")
    key = items[0].strip()
    value = None
    if len(items) > 1:
        value = "=".join(items[1:])
    return key, value


def parse_vars(items: List[str]) -> Dict[str, str]:
    """ Parse a list of key value pairs"""
    result = {}
    for item in items:
        key, value = parse_var(item)
        result[key] = value
    return result


def print_header(text: str, color: Optional[str] = None, sep: str = "="):
    """ Print a header line with text in the middle """
    size = os.get_terminal_size()
    width_segment = floor((size.columns / 2) - (len(text) + 2) / 2)
    segment = sep * width_segment
    color_str = color if color is not None else ""
    color_str_end = COLOR_RESET if color is not None else ""
    print(f"{color_str}{segment} {text} {segment}{color_str_end}")
