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
- my-file.json
        rule_keys_are_sorted

# Lint multiple files...
$ json-linter a.json b.json
- a.json
        rule_keys_are_sorted
+ b.json

# Lint all files in a directory
$ json-linter files
- files/a.json
        rule_keys_are_sorted
+ files/b.json

# Lint all files in a directory recursively
$ json-linter files --recursive
- files/in/a/subdirectory/a.json
        rule_keys_are_sorted
# ...

# Lint all files in a directory recursively with .config and .cfg ending
$ json-linter files -r --extensions cfg config
- files/in/a/subdirectory/a.cfg
        rule_keys_are_sorted
+ files/in/a/subdirectory/b.config
# ...

# Fix files (will overwrite the file with a fixed version and then lint)
$ json-linter my-file.json --fix
+ my-file.json

# Overwrite configuration values
$ json-linter my-file.json --config-set naming_style=KEBAB_CASE indent=2
```

## License

GNU General Public License v3

![](https://www.gnu.org/graphics/gplv3-127x51.png)
