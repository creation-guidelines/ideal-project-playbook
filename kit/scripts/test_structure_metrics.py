#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 grenudi
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Tests for structure-metrics.py. Plain asserts, no framework: ``python3 kit/scripts/test_structure_metrics.py``."""
import importlib.util
import os
import sys
import tempfile
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("sm", os.path.join(HERE, "structure-metrics.py"))
sm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sm)


def tree(files):
    root = tempfile.mkdtemp()
    for path, text in files.items():
        full = os.path.join(root, "src", path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, "w").write(text)
    return root


def lines(n):
    return "\n".join(f"x{i} = {i}" for i in range(n)) + "\n"


def test_the_size_measures_and_the_huddled_range_stop_at_299():
    # a file's size is len(text.split("\\n")), the original's convention: a trailing newline counts one. So: 299, 301 and 300 lines.
    root = tree({"a.py": '"""Does a."""\n' + lines(297), "b.py": '"""Does b."""\n' + lines(299), "c.py": '"""Does c."""\n' + lines(298)})
    m = sm.measure(root, ["src"])
    assert m["source files"] == 3 and m["files over 300"] == 1 and m["files 250-299 (huddled under the limit)"] == 1, m
    assert m["biggest file"] == 301 and m["median file (lines)"] == 300, m  # 300 is neither huddled nor over


def test_test_files_and_inline_test_modules_are_not_production_code():
    root = tree({"a.rs": "//! Does a.\nfn f() {}\n#[cfg(test)]\nmod tests {\n" + "    fn t() {}\n" * 400 + "}\n",
                 "tests/b.rs": lines(500), "test_c.py": lines(500), "d.test.ts": lines(500)})
    m = sm.measure(root, ["src"])
    assert m["source files"] == 1 and m["biggest file"] == 2, m


def test_a_long_function_is_counted_by_its_balanced_braces_and_a_brace_in_a_string_is_not_code():
    body = "    let x = 1;\n" * 70
    long_fn = "fn long() {\n" + body + "}\n"
    tricky = "fn short() {\n    let s = \"}\";\n    let c = '}';\n    // }\n}\nfn also_short() {\n    1\n}\n"
    assert sm.long_functions("a.rs", long_fn) == 1
    assert sm.long_functions("a.rs", tricky) == 0, "a brace in a string, a character or a comment does not end a function"
    py = "def f():\n" + "    x = 1\n" * 70 + "def g():\n    return 1\n"
    assert sm.long_functions("a.py", py) == 1


def test_modules_without_a_purpose_and_with_jargon_are_counted():
    root = tree({"a.py": '"""An adapter that talks to the thing."""\n', "b.py": "x = 1\n", "c.py": '"""Draws the header."""\n'})
    m = sm.measure(root, ["src"])
    assert m["modules with no purpose sentence"] == 1 and m["purposes in pattern jargon"] == 1, m


TESTS = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]

if __name__ == "__main__":
    failed = 0
    for t in TESTS:
        try:
            t()
            print("ok  ", t.__name__)
        except Exception:
            failed += 1
            print("FAIL", t.__name__)
            traceback.print_exc()
    print(f"{len(TESTS) - failed}/{len(TESTS)} passed")
    sys.exit(1 if failed else 0)
