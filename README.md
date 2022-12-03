# json-linter

Lint your JSON files!

## Features

* Check if keys are sorted alphabetically...
* Check if your keys are either in camelCase, snake\_case or kebab-case...
* ...and automatically fix (some) of these issues!

## Install

You need to have Python 3.10+ installed.

```bash
$ pip install json-linter
```

## Usage

```bash
# Lint a single file...
$ json-linter my-file.json

# Lint multiple files...
$ json-linter a.json b.json

# Lint all files in a directory
$ json-linter files

# Lint all files in a directory recursively
$ json-linter files --recursive

# Lint all files in a directory recursively with .config and .cfg ending
$ json-linter files -r --extensions cfg config

# Fix files (will overwrite the file with a fixed version and then lint)
$ json-linter my-file.json --fix

# Overwrite configuration values
$ json-linter my-file.json --config-set naming_style=KEBAB_CASE indent=2

# Return results as json
$ json-linter my-file.json --json
```

### Use as a package

```python
from pathlib import Path

from json_linter import lint_file


results = lint_file(Path("./my-file.json"))

for result in results:
    if not result.was_successful:
        print(result.path, "failed!")

```

## License

GNU General Public License v3

![](https://www.gnu.org/graphics/gplv3-127x51.png)
