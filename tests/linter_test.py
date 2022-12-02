from pathlib import Path
from typing import List

from json_linter.config import NamingStyle
from json_linter.linter import lint_file, apply_fixes, DEFAULT_CONFIG, \
    LinterResult


def _fixture(name: str) -> Path:
    return Path(Path(__file__).parent, "__fixtures__", name)


def _did_any_rule_fail(results: List[LinterResult]) -> bool:
    for res in results:
        if not res.was_successful:
            return False
    return True


def test_linting_fixtures():
    def lint_fixture(fixture: str, success: bool):
        results = lint_file(_fixture(fixture))
        assert _did_any_rule_fail(results) == success

    lint_fixture("fixed-keys-sorted-array.json", True)
    lint_fixture("fixed-keys-sorted-object.json", True)
    lint_fixture("fixed-keys-sorted-z-before-a.json", True)
    lint_fixture("keys-sorted-array.json", False)
    lint_fixture("keys-sorted-object.json", False)
    lint_fixture("keys-sorted-z-before-a.json", False)
    lint_fixture("test-utf8.json", True)


def test_fixing_fixtures():
    def fix_fixture(fixture: str):
        data = _fixture(fixture).read_text()
        fixed = _fixture(f"fixed-{fixture}").read_text()
        data_fixed = apply_fixes(data)
        assert data_fixed == fixed

    fix_fixture("keys-sorted-array.json")
    fix_fixture("keys-sorted-object.json")
    fix_fixture("keys-sorted-z-before-a.json")


def test_utf8_unchanged():
    data = _fixture("test-utf8.json").read_text()
    fixed_data = apply_fixes(data)
    assert data == fixed_data


def test_name_style_lints():
    def lint_fixture(fixture: str, naming_style: NamingStyle, success: bool):
        config = DEFAULT_CONFIG
        config.naming_style = naming_style
        results = lint_file(_fixture(fixture), config)
        assert _did_any_rule_fail(results) == success

    # the right files are correct
    lint_fixture(
        "naming-style-is-correct-camel-case.json",
        NamingStyle.CAMEL_CASE,
        True,
    )
    lint_fixture(
        "naming-style-is-correct-kebab.json",
        NamingStyle.KEBAB_CASE,
        True,
    )
    lint_fixture(
        "naming-style-is-correct-snake-case.json",
        NamingStyle.SNAKE_CASE,
        True,
    )

    # check if non camel case files fail
    lint_fixture(
        "naming-style-is-correct-kebab.json",
        NamingStyle.CAMEL_CASE,
        False,
    )
    lint_fixture(
        "naming-style-is-correct-snake-case.json",
        NamingStyle.CAMEL_CASE,
        False,
    )

    # check if non kebab case files fail
    lint_fixture(
        "naming-style-is-correct-camel-case.json",
        NamingStyle.KEBAB_CASE,
        False,
    )
    lint_fixture(
        "naming-style-is-correct-snake-case.json",
        NamingStyle.KEBAB_CASE,
        False,
    )

    # check if non snake case files fail
    lint_fixture(
        "naming-style-is-correct-camel-case.json",
        NamingStyle.SNAKE_CASE,
        False,
    )
    lint_fixture(
        "naming-style-is-correct-kebab.json",
        NamingStyle.SNAKE_CASE,
        False,
    )
