#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 grenudi
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Generalised from snapall's dev/structure-metrics.py: language-neutral, with the source folders as options.

"""How the shape of the code changes over time, so progress is a number and not an impression.

    structure-metrics.py [REF ...] [--src DIR]...          (default: compare the working tree with nothing)

Each REF is a git tag, branch or commit (``WORKTREE`` is the files as they are now). For each it measures: source files, the median
file, files over 300 lines and those huddled just under (250 to 299), the biggest file, functions over 60 lines, modules with no
purpose sentence, and purposes written in pattern jargon (adapter, port, hexagon, shell, driving). Run it against the tag from the
start of the work and report the trend in plain words. A number can be gamed (split a file without making it clearer); that is why it
sits beside the stranger test, never instead of it.

Compare like with like: the counts of long functions and of jargon use this script's own definitions (a function ends where its braces balance, ignoring braces in
strings and comments), so they differ by a constant from another tool's. On snapall, the original script reports functions over 60 lines going 29 to 25 and this one 25 to 21,
the same four fewer; files, median, files over 300 and the huddled range match exactly.
"""
import ast
import os
import re
import statistics
import subprocess
import sys
import tarfile
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "guards"))
from outline import EXTENSIONS, SKIP_FILES, purpose  # noqa: E402

JARGON = re.compile(r"(adapter|imperative|\bshell\b|hexagon|composition root|functional core|driving|\bport\b)", re.I)
TESTS = ("/tests/", "/test/", "/__tests__/", "test_", "_test.", ".test.", ".spec.", "tests.rs")
STOP_AT = "#[cfg(test)]"
LITERAL = re.compile(r'r#*"[^"]*"#*|"(?:\\\\.|[^"\\\\])*"|\'(?:\\\\.|[^\'\\\\])\'|//.*$')
FUNCTION = re.compile(r"^\s*(pub(\([a-z]+\))?\s+)?(async\s+)?(fn|func|function)\b")


def files(root, sources):
    for src in sources:
        for directory, _, names in os.walk(os.path.join(root, src)):
            if any(p.startswith(".") and p != "." or p in ("node_modules", "target") for p in os.path.relpath(directory, root).split(os.sep)):
                continue
            for name in names:
                path = os.path.join(directory, name)
                rel = os.path.relpath(path, root)
                if name.rsplit(".", 1)[-1] in EXTENSIONS and not any(t in "/" + rel for t in TESTS):
                    text = open(path, encoding="utf-8", errors="replace").read()
                    if STOP_AT.replace("#[", "#![") in text:  # a whole file of test code, as Rust marks it
                        continue
                    yield rel, text.split("\n" + STOP_AT)[0]  # production code only: Rust keeps its tests below this line


def long_functions(path, text, limit=60):
    if path.endswith(".py"):
        try:
            tree = ast.parse(text)
        except SyntaxError:
            return 0
        return sum(1 for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.end_lineno - n.lineno + 1 > limit)
    count, lines = 0, [LITERAL.sub('""', line) for line in text.split("\n")]  # a brace inside a string or a character is not code
    for i, line in enumerate(lines):
        if FUNCTION.match(line) and "{" in "".join(lines[i:i + 5]):
            depth, started = 0, False
            for j in range(i, len(lines)):
                depth += lines[j].count("{") - lines[j].count("}")
                started = started or "{" in lines[j]
                if started and depth <= 0:
                    count += (j - i + 1) > limit
                    break
    return count


def measure(root, sources):
    found = list(files(root, sources))
    sizes = [len(text.split("\n")) for _, text in found]
    modules = [(p, purpose(p, t)) for p, t in found if os.path.basename(p) not in SKIP_FILES]
    return {
        "source files": len(found),
        "median file (lines)": int(statistics.median(sizes)) if sizes else 0,
        "files over 300": sum(s > 300 for s in sizes),
        "files 250-299 (huddled under the limit)": sum(250 <= s <= 299 for s in sizes),
        "biggest file": max(sizes, default=0),
        "functions over 60 lines": sum(long_functions(p, t) for p, t in found),
        "modules with no purpose sentence": sum(1 for _, p in modules if not p),
        "purposes in pattern jargon": sum(1 for _, p in modules if p and JARGON.search(p)),
    }


def checkout(ref):
    if ref == "WORKTREE":
        return "."
    out = tempfile.mkdtemp()
    data = subprocess.run(["git", "archive", ref], capture_output=True, check=True).stdout
    with tempfile.TemporaryFile() as f:
        f.write(data)
        f.seek(0)
        tarfile.open(fileobj=f).extractall(out, filter="data")
    return out


def main(argv):
    sources = [argv[i + 1] for i, a in enumerate(argv) if a == "--src" and i + 1 < len(argv)] or (["src"] if os.path.isdir("src") else ["."])
    taken = {i for i, a in enumerate(argv) if a == "--src"} | {i + 1 for i, a in enumerate(argv) if a == "--src"}
    refs = [a for i, a in enumerate(argv) if i not in taken] or ["WORKTREE"]
    results = [(ref, measure(checkout(ref), sources)) for ref in refs]
    width = max(len(k) for k in results[0][1])
    print(" " * (width + 2) + "".join(f"{ref[:12]:>14}" for ref, _ in results))
    for key in results[0][1]:
        print(f"{key:<{width + 2}}" + "".join(f"{r[key]:>14}" for _, r in results))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
