#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""check_paths.py - a document that names a file of this repository names one that exists.

    python3 tools/check_paths.py

A path written as a literal (double backticks) in any reStructuredText file is checked when it looks like a file of this repository: it
starts with one of this repository's directories, or is a file in the root, and has an extension. A path that is only an example, or
belongs to another project, is written as a link (to that project) or with a placeholder (``<name>``, ``*``), and is not checked.
This is the playbook's own rule, "documents tell the truth", applied to the playbook."""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRS = ("kit/", "playbook/", "tools/", "bin/", "data/", ".github/", "docs/")
EXTENSIONS = (".rst", ".py", ".sh", ".json", ".sql", ".yml", ".yaml", ".md", ".txt", ".js")
LITERAL = re.compile(r"(?<!`)``([^`\n]+)``(?!`)")


def looks_like_a_path_here(text):
    if re.search(r"[\s<>*$(){}=,;]", text) or not text.endswith(EXTENSIONS) or (text.startswith(".") and "/" not in text):
        return False  # (an extension on its own, such as ``.rst``, is not a path)
    return text.startswith(DIRS) or "/" not in text


def main():
    # the templates name the files of a project that does not exist yet, so they are not checked against this repository
    files = sorted(f for f in glob.glob(os.path.join(ROOT, "**", "*.rst"), recursive=True) if "/.git/" not in f and "/node_modules/" not in f and "/kit/templates/" not in f)
    missing, checked = [], 0
    for path in files:
        for number, line in enumerate(open(path, encoding="utf-8").read().split("\n"), 1):
            for text in LITERAL.findall(line):
                if looks_like_a_path_here(text):
                    checked += 1
                    if not os.path.exists(os.path.join(ROOT, text)):
                        missing.append(f"{os.path.relpath(path, ROOT)}:{number}: ``{text}`` does not exist")
    for line in missing:
        print("MISSING", line)
    print(f"{checked} paths named in {len(files)} documents; {len(missing)} do not exist")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
