#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 grenudi
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Generalised from snapall's dev/find-duplicates.py (which read Rust only): the files, the comment prefixes and what counts as a
# test file are options, and the defaults cover the common languages.

"""Find the same code written in more than one place.

    find-duplicates.py [--glob PATTERN]... [--comment PREFIXES] [--skip SUBSTRINGS] [--lines N] [--min-chars C] [--top T] [--near]

A rule copied by hand is a rule that can come out differently in each copy, and it is the commonest thing a reading of the code
finds. Reading finds them one module at a time; this finds them all at once. It looks at production code only (tests repeat on
purpose), drops comments and the lines that carry no meaning on their own (brackets and closers such as `});`, imports, annotations), and reports every
run of N lines (default 4) that appears in two or more places, longest and most repeated first. With --near, names, numbers and
strings are forgotten and only the shape is compared: the same code under different names, which is how a rule gets copied and
then renamed to fit. A repeated run is a candidate, not a verdict: two commands that begin the same way may be right to. Read each,
and name the rule if there is one.

    --glob PATTERN     files to scan, repeatable (default: common source files under src/, or under . when there is no src/)
    --comment P1,P2    line-comment prefixes to drop (default: // # --)
    --skip A,B         a file is a test, and skipped, if its path holds one of these (default: /tests/,/test/,/__tests__/,test_,_test.,.test.,.spec.,tests.rs)
    --stop-at LINE     in a file, everything from a line starting with this on is test code (default: #[cfg(test)], Rust's inline test module)
"""
import collections, glob, os, re, sys

TRIVIAL = re.compile(r"^([\]\[(){};,.]+|\)\.collect\(\);?|else \{|else:|((pub(\([a-z]+\))? )?(use|mod)|import|from|using|package|#include|@|#\[).*)$")
KEYWORDS = set("""as break case catch class const continue crate def default defer do elif else enum except export extends false final finally fn for from func
function go if impl import in interface is let lambda loop match mod move mut new nil none None not null of or and pass pub raise ref return self Self static struct
super switch throw trait true True False try type typeof unsafe use var void where while with yield async await""".split())
EXTENSIONS = "py rs ts tsx js jsx go java kt scala c cc cpp h hpp cs rb php swift sh".split()


def shape(line):
    """The line with its names, numbers and strings forgotten: what is left is how it is built."""
    line = re.sub(r'"(?:\\.|[^"\\])*"', '"S"', line)
    line = re.sub(r"'(?:\\.|[^'\\])*'", "'S'", line)
    line = re.sub(r"\b\d[\d_]*(?:\.\d+)?\b", "N", line)
    return re.sub(r"\b[A-Za-z_]\w*\b", lambda m: m.group(0) if m.group(0) in KEYWORDS else "I", line)


def options(argv):
    def values(name):
        return [argv[i + 1] for i, a in enumerate(argv) if a == f"--{name}" and i + 1 < len(argv)]
    one = lambda name, default: (values(name) or [default])[-1]
    return {
        "globs": values("glob"),
        "comment": tuple(one("comment", "//,#,--").split(",")),
        "skip": tuple(one("skip", "/tests/,/test/,/__tests__/,test_,_test.,.test.,.spec.,tests.rs").split(",")),
        "window": int(one("lines", "4")), "min_chars": int(one("min-chars", "170")), "top": int(one("top", "25")),
        "stop_at": one("stop-at", "#[cfg(test)]"),
        "near": "--near" in argv,
    }


def default_globs():
    root = "src" if os.path.isdir("src") else "."
    return [f"{root}/**/*.{ext}" for ext in EXTENSIONS]


def production_lines(path, comment, skip, stop_at):
    if any(part in "/" + path for part in skip):
        return []
    try:
        text = open(path, encoding="utf-8").read()
    except (UnicodeDecodeError, OSError):
        return []
    if stop_at.replace("#[", "#![") in text:  # a whole file of test code, as Rust marks it
        return []
    out = []
    for number, line in enumerate(text.split("\n"), 1):
        norm = " ".join(line.split())
        if stop_at and norm.startswith(stop_at):
            break
        if not norm or norm.startswith(comment) or TRIVIAL.match(norm):
            continue
        out.append((number, norm))
    return out


def scan(files, opt):
    seen = collections.defaultdict(list)
    for path in files:
        lines = production_lines(path, opt["comment"], opt["skip"], opt["stop_at"])
        for at in range(len(lines) - opt["window"] + 1):
            chunk = lines[at: at + opt["window"]]
            body = "\n".join(text for _, text in chunk)
            if len(body) >= opt["min_chars"]:
                key = shape(body) if opt["near"] else body
                seen[key].append((path, chunk[0][0], chunk[-1][0], body))
    found = []
    for body, places in seen.items():
        if len(places) < 2:
            continue
        # near: the same shape under different names; the identical ones are the exact scan's
        if opt["near"] and len({original for *_, original in places}) < 2:
            continue
        found.append((len(places) * len(body), body, places))
    found.sort(key=lambda item: -item[0])
    return found


def main(argv):
    opt = options(argv)
    files = sorted({f for pattern in (opt["globs"] or default_globs()) for f in glob.glob(pattern, recursive=True) if os.path.isfile(f)})
    found = scan(files, opt)
    reported, shown = [], 0
    for weight, body, places in found:
        # a longer run reports its overlapping shorter ones too: show each place once
        if any(any(p[0] == q[0] and p[1] <= q[2] and q[1] <= p[2] for p in places for q in earlier) for earlier in reported):
            continue
        reported.append(places)
        shown += 1
        print(f"\n{len(places)}x  ({len(body)} chars)")
        for path, first, last, _ in places:
            print(f"    {path}:{first}-{last}")
        for line in (places[0][3] if opt["near"] else body).split("\n")[:opt["window"]]:
            print(f"      | {line[:110]}")
        if shown >= opt["top"]:
            break
    print(f"\n{len(found)} repeated runs of {opt['window']} lines; {shown} shown")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
