#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""check_rst.py - every reStructuredText file in the repository is valid, and no warning is let through.

    python3 tools/check_rst.py            check every *.rst (the generated pages in docs/ included)

Docutils is run with a report level of "warning" and a halt level of "warning", so anything it would only warn
about (a bad underline, an unknown directive, an inconsistent list) fails here. Informational messages, such as a
link target that nothing references, are not problems."""
import glob
import io
import os
import sys

from docutils.core import publish_doctree

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def problems(path):
    stream = io.StringIO()
    try:
        publish_doctree(open(path, encoding="utf-8").read(), source_path=path,
                        settings_overrides={"report_level": 2, "halt_level": 2, "warning_stream": stream})
    except Exception as error:  # docutils halts with an exception at the halt level
        return f"{error}\n{stream.getvalue()}".strip()
    return stream.getvalue().strip()


def main():
    files = sorted(f for f in glob.glob(os.path.join(ROOT, "**", "*.rst"), recursive=True)
                   if "/node_modules/" not in f and "/.git/" not in f)
    bad = 0
    for path in files:
        found = problems(path)
        if found:
            bad += 1
            print(f"FAIL {os.path.relpath(path, ROOT)}\n    " + found.replace("\n", "\n    "))
    print(f"{len(files) - bad} of {len(files)} reStructuredText files are valid")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
