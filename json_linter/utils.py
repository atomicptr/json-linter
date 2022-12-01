""" Utility functions """
from importlib import import_module
from pathlib import Path
from types import ModuleType
from typing import List

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
