""" Linter configuration """
from dataclasses import dataclass
from typing import Optional


@dataclass
class LinterConfig:
    """ Configuration for the linter/fixer """
    indent: int
    naming_style: Optional[str]
