""" Linter configuration """
from dataclasses import dataclass
from enum import Enum
from typing import Optional

NamingStyle = Enum("NamingStyle", [
    "camel-case",
    "snake-case",
    "kebab-case",
])


@dataclass
class LinterConfig:
    """ Configuration for the linter/fixer """
    indent: int
    naming_style: Optional[NamingStyle]
    encoding: str
