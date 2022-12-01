from dataclasses import dataclass
from typing import Optional


@dataclass
class LinterResult:
    """ Result of a linter operation"""
    name: str
    path: str
    was_successful: bool
    error_message: Optional[str]
    was_exception: bool


@dataclass
class LinterConfig:
    indent: int
    naming_style: Optional[str]
