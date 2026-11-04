#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 grenudi
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Generalised from snapall's dev/sample-modules.py: the layers and the files are options, and the defaults cover common languages.

"""Pick modules at random to read as a stranger, because that finds what no guard measures.

    sample-modules.py [SEED] [PER_LAYER] [--layer NAME=DIR]... [--min-lines N] [--max-lines N] [--stop-at LINE]

The proxies (sizes, the outline, the findability test) are all things someone thought to measure. Reading code with no memory of
having written it finds what nobody thought of: stale words in messages, a rule copied by hand, the same sentence written twice.
Sampling at random, with a seed so a read can be reproduced, keeps the choice from drifting to the modules already liked.

It picks modules of a size worth judging (80 to 300 lines of production code by default) from each layer. A layer is a directory
(--layer core=src/core, repeatable); with none given, each directory directly under src/ is a layer, or the whole tree is one. Index
files (mod.rs, lib.rs, main.rs, __init__.py, index.ts) and test files are never picked. The default seed is today's date.

Read each module in full, then write down what a stranger would notice, and fix what is real. When a seed returns modules you have
already read, the method is exhausted: say so, and read differently (use the program as a newcomer would).
"""
import datetime, glob, os, random, sys

EXTENSIONS = "py rs ts tsx js jsx go java kt scala c cc cpp h hpp cs rb php swift sh".split()
INDEX_FILES = {"mod.rs", "lib.rs", "main.rs", "__init__.py", "index.ts", "index.js", "index.tsx", "__main__.py"}
TEST_MARKERS = ("/tests/", "/test/", "/__tests__/", "test_", "_test.", ".test.", ".spec.", "tests.rs")


def layers(opt_layers):
    if opt_layers:
        return dict(item.split("=", 1) for item in opt_layers)
    root = "src" if os.path.isdir("src") else "."
    sub = [d for d in sorted(os.listdir(root)) if os.path.isdir(os.path.join(root, d)) and not d.startswith(".")] if root == "src" else []
    return {d: os.path.join(root, d) for d in sub} or {"all": root}


def modules(directory, lo, hi, stop_at):
    found = []
    for ext in EXTENSIONS:
        for path in sorted(glob.glob(os.path.join(directory, f"**/*.{ext}"), recursive=True)):
            if os.path.basename(path) in INDEX_FILES or any(m in "/" + path for m in TEST_MARKERS):
                continue
            try:
                text = open(path, encoding="utf-8").read()
            except (UnicodeDecodeError, OSError):
                continue
            if stop_at.replace("#[", "#![") in text:
                continue
            lines = len(text.split(stop_at)[0].split("\n")) if stop_at else len(text.split("\n"))
            if lo <= lines <= hi:
                found.append((path, lines))
    return found


def main(argv):
    values = lambda name: [argv[i + 1] for i, a in enumerate(argv) if a == f"--{name}" and i + 1 < len(argv)]
    one = lambda name, default: (values(name) or [default])[-1]
    taken = {i for i, a in enumerate(argv) if a.startswith("--")} | {i + 1 for i, a in enumerate(argv) if a.startswith("--")}
    positional = [a for i, a in enumerate(argv) if i not in taken]
    seed = int(positional[0]) if positional else int(datetime.date.today().strftime("%Y%m%d"))
    per_layer = int(positional[1]) if len(positional) > 1 else 2
    lo, hi, stop_at = int(one("min-lines", "80")), int(one("max-lines", "300")), one("stop-at", "#[cfg(test)]")
    random.seed(seed)
    print(f"seed {seed}")
    for name, directory in layers(values("layer")).items():
        files = modules(directory, lo, hi, stop_at)
        for path, lines in random.sample(files, min(per_layer, len(files))):
            print(f"{name:12} {lines:4}  {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
