""" CLI for json_linter """
import argparse
import sys
from dataclasses import fields
from typing import List, Dict

from json_linter.config import LinterConfig
from json_linter.files import gather_files
from json_linter.linter import fix, lint, LinterResult, DEFAULT_CONFIG
from json_linter.utils import flatten, COLOR_RED, COLOR_GREEN, COLOR_RESET, \
    parse_vars


def main():
    """ Main function for CLI """
    parser = argparse.ArgumentParser(
        prog="json-linter",
        description="Lint your JSON files!",
    )

    parser.add_argument(
        "filename",
        type=str,
        nargs="+",
        help="filenames or directories to lint or format",
        action="append"
    )
    parser.add_argument(
        "-r", "--recursive",
        help="walk through subdirectories recursively",
        action="store_true"
    )
    parser.add_argument(
        "-v", "--verbose",
        help="show verbose output",
        action="store_true"
    )
    parser.add_argument(
        "-q", "--quiet",
        help="remove all output, even if verbose is set",
        action="store_true"
    )
    parser.add_argument(
        "--extensions",
        type=str,
        nargs="+",
        help="file extensions to look for, by default only json",
        action="append"
    )
    parser.add_argument(
        "--fix",
        help="fix and format files",
        action="store_true"
    )
    config_options_str = ", ".join(
        [field.name for field in fields(LinterConfig)]
    )
    parser.add_argument(
        "--config-set",
        nargs="+",
        help="Set configuration options via key-value pairs "
             "(do not put spaces before or after the = sign). "
             "If a value contains spaces, you should define it with double "
             "quotes: 'foo=\"this is an example\". "
             f"Configuration options are: {config_options_str}."
    )

    args = parser.parse_args(sys.argv[1:])

    def log(*func_args):
        """ Logs things unless quiet """
        if args.quiet:
            return
        print(*func_args)

    config = DEFAULT_CONFIG

    if args.config_set is not None and len(args.config_set) > 0:
        config_vars = parse_vars(args.config_set)

        for key in config_vars:
            if not hasattr(config, key):
                log(
                    f"Invalid configuration key provided: '{key}', "
                    f"options are: {config_options_str}"
                )
                sys.exit(1)

        config.set_values(config_vars)

    if args.verbose:
        log("Arguments:", args)

    files = flatten([
        gather_files(filename, flatten(args.extensions), args.recursive)
        for filename in flatten(args.filename)
    ])

    if len(files) == 0:
        log("No files found.")
        sys.exit(1)

    if args.verbose and len(files) > 0:
        files_str = "\n* ".join(map(str, files))
        log(f"Files:\n* {files_str}")

    if args.fix:
        fix(files)

    linter_results = lint(files)

    file_results: Dict[str, List[LinterResult]] = {}
    has_error = False

    for result in linter_results:
        if result.path not in file_results:
            file_results[result.path] = []

        if not result.was_successful:
            has_error = True
            file_results[result.path].append(result)

    if args.verbose and len(linter_results) > 0:
        log("Results:")

    for file in sorted(file_results.keys()):
        has_issue = len(file_results[file]) > 0
        list_item = "-" if has_issue else "+"

        color = COLOR_RED if has_issue else COLOR_GREEN

        log(f"{color}{list_item} {file}{COLOR_RESET}")

        for result in file_results[file]:
            err_text = " (!)" if result.was_exception else ""
            message = "" if result.error_message is None else \
                f": {result.error_message}"
            log(f"\t{COLOR_RED}{result.name}{message}{err_text}{COLOR_RESET}")

    if has_error:
        sys.exit(1)
