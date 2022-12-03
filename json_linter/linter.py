""" Lint/Fix files """
import json
from dataclasses import dataclass, fields
from pathlib import Path
from typing import List, Optional

from json_linter.fixers import get_all_fixers
from json_linter.rules import get_all_rules
from json_linter.config import LinterConfig

DEFAULT_CONFIG = LinterConfig(
    indent=4,
    naming_style=None,
    encoding="utf-8",
)


@dataclass
class LinterResult:
    """ Result of a linter operation"""
    name: str
    path: str
    was_successful: bool
    error_message: Optional[str]
    was_exception: bool

    def to_dict(self):
        """ Return linter result as a dictionary """
        new_dict = {}
        for field in fields(self):
            new_dict[field.name] = getattr(self, field.name)
        return new_dict


def lint(
    files: List[Path],
    config: LinterConfig = DEFAULT_CONFIG
) -> List[LinterResult]:
    """ Lint a list of files and return results """
    linter_results = []
    for file in files:
        linter_results.extend(lint_file(file, config))
    return linter_results


def lint_file(
    file_path: Path,
    config: LinterConfig = DEFAULT_CONFIG
) -> List[LinterResult]:
    """ Lint a single file """
    data = file_path.read_text(encoding=config.encoding)

    try:
        json_data = json.loads(data)
    except Exception as err:
        return [LinterResult(
            name="lint_file",
            path=str(file_path.relative_to(Path.cwd())),
            was_successful=False,
            error_message=f"{type(err).__name__}: {str(err)}",
            was_exception=True,
        )]

    results = []

    for rule in get_all_rules():
        res = LinterResult(
            name=rule.__name__,
            path=str(file_path.relative_to(Path.cwd())),
            was_successful=True,
            error_message=None,
            was_exception=False,
        )

        try:
            success, message = rule(json_data, config)
            if not success:
                res.was_successful = success
                res.error_message = message
        except Exception as err:
            res.was_successful = False
            res.error_message = f"{type(err).__name__}: {str(err)}"
            res.was_exception = True

        results.append(res)

    return results


def fix(files: List[Path], config: LinterConfig = DEFAULT_CONFIG) -> None:
    """ Fix a list of files """
    for file in files:
        fix_file(file, config)


def fix_file(file_path: Path, config: LinterConfig = DEFAULT_CONFIG) -> None:
    """ Fix a single file """
    data = file_path.read_text()
    file_path.write_text(
        apply_fixes(data, config),
        encoding=config.encoding,
    )


def apply_fixes(data: str, config: LinterConfig = DEFAULT_CONFIG) -> str:
    """ Apply fixes to a string and return it """
    for fixer in get_all_fixers():
        data = fixer(data, config)

    obj = json.loads(data)

    return json.dumps(
        obj,
        indent=config.indent,
        sort_keys=True,
        ensure_ascii=False,
    )
