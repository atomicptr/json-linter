from pathlib import Path

from json_linter.linter import lint_file, apply_fixes


def _fixture(name: str) -> Path:
    return Path(Path(__file__).parent, "__fixtures__", name)


def test_linting_fixtures():
    def lint_fixture(fixture: str, success: bool = True):
        results = lint_file(_fixture(fixture))

        for res in results:
            assert res.was_successful == success

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
