from pathlib import Path

from json_linter.linter import lint_file


def _fixture(name: str) -> Path:
    return Path(Path(__file__).parent, "__fixtures__", name)


def _lint_fixture(fixture: str, success: bool = True):
    results = lint_file(_fixture(fixture))

    for res in results:
        assert res.was_successful == success


def test_fixtures():
    _lint_fixture("fixed-keys-sorted-array.json", True)
    _lint_fixture("fixed-keys-sorted-object.json", True)
    _lint_fixture("fixed-keys-sorted-z-before-a.json", True)
    _lint_fixture("keys-sorted-array.json", False)
    _lint_fixture("keys-sorted-object.json", False)
    _lint_fixture("keys-sorted-z-before-a.json", False)
