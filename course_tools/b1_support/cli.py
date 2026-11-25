"""Explicit B1 CLI. No scanning, writing, or argument parsing on import."""

import argparse
import sys
from pathlib import Path

if __name__ == "__main__" and not __package__:
    # Support the handbook's direct-script command, independent of the cwd.
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from course_tools.b1_support.manifest_builder import build_manifest
from course_tools.b1_support.report_writer import validate_output_path, write_report


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Read-only inventory and explicit B1 reports")
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("scan", "stats", "manifest"):
        subparser = commands.add_parser(command)
        subparser.add_argument("directory", help="Directory to inspect")
        subparser.add_argument("--output", required=True, help="New report file in an allowed location")
        subparser.add_argument("--format", choices=("json", "csv", "markdown"), default="json")
        subparser.add_argument("--exclude", action="append", default=[], help="Repeatable relative glob")
        subparser.add_argument("--include", action="append", default=[], help="Repeatable relative glob")
    args = parser.parse_args(argv)
    try:
        output = validate_output_path(args.output)
        root = Path(args.directory).resolve()
        omitted = (output.relative_to(root).as_posix(),) if output.is_relative_to(root) else ()
        report = build_manifest(root, detail=args.command, include=args.include,
                                exclude=args.exclude, omit_paths=omitted)
        write_report(report, output=output, format=args.format)
    except (OSError, ValueError, RuntimeError):
        # Avoid echoing machine paths, source contents, or OS exception messages.
        parser.exit(2, "error: invalid input/output, existing output, or inaccessible filesystem\n")
    print("Report written successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
