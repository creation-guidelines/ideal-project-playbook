#!/bin/bash
# SPDX-FileCopyrightText: 2026 grenudi
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Generalised from snapall's dev/golden-output.sh: the commands, the fixture and what is unstable are files and hooks you give it.
#
# What a program prints, for a fixed list of commands: text, JSON, error messages and exit codes, with what changes from run to run
# (dates, counts, versions) made stable. A refactoring that must not change behaviour is shown not to by `check` passing before and
# after it, and a change to wording shows as the few lines that moved.
#
#   golden-output.sh record PROGRAM COMMANDS   write what the program prints to $GOLDEN_DIR (default golden/)
#   golden-output.sh check  PROGRAM COMMANDS   run again and compare; exits 1 on any difference
#
# COMMANDS is a file with one command line per line (the arguments, without the program). Optional, as environment variables:
#   GOLDEN_FIXTURE_UP / GOLDEN_FIXTURE_DOWN   commands that build and tear down what the program runs against (a disk, a service, a
#                                             database); down runs first and last, so every run starts from the same state
#   GOLDEN_NORMALIZE                          a sed script file that makes unstable text stable (dates, ids, timings)
#   GOLDEN_DIR                                where the recordings live (golden/)
#
# Two safeguards that exist because of mistakes: it refuses to run when the program cannot be found, and it refuses to *record* an
# output that is empty or is only "command not found" or "permission denied". A recording of nothing once looked like a clean change
# (1,096 deleted lines across twenty files) until somebody read the diff. Read the diff of a recording before you commit it.
set -u
mode=${1:?usage: golden-output.sh record|check PROGRAM COMMANDS}
program=${2:?usage: golden-output.sh record|check PROGRAM COMMANDS}
commands=${3:?usage: golden-output.sh record|check PROGRAM COMMANDS}
golden=${GOLDEN_DIR:-golden}

[ -x "$program" ] || command -v "$program" >/dev/null 2>&1 || { echo "golden-output: the program '$program' cannot be run from here"; exit 2; }
[ -f "$commands" ] || { echo "golden-output: no commands file '$commands'"; exit 2; }
program=$(command -v "$program" 2>/dev/null || realpath "$program")

[ -n "${GOLDEN_FIXTURE_DOWN:-}" ] && { bash -c "$GOLDEN_FIXTURE_DOWN" >/dev/null 2>&1; bash -c "$GOLDEN_FIXTURE_DOWN" >/dev/null 2>&1; }
[ -n "${GOLDEN_FIXTURE_UP:-}" ] && { bash -c "$GOLDEN_FIXTURE_UP" >/dev/null || { echo "golden-output: the fixture would not come up"; exit 2; }; }

out=$(mktemp -d)   # always a fresh directory: a recording replaces $golden only once it has been checked

stable() { if [ -n "${GOLDEN_NORMALIZE:-}" ]; then sed -E -f "$GOLDEN_NORMALIZE"; else cat; fi; }

while IFS= read -r command; do
  [ -z "$command" ] && continue
  name=$(echo "$command" | tr ' /' '__')
  { "$program" $command </dev/null 2>&1; echo "exit: $?"; } | stable > "$out/$name.txt"
done < "$commands"

[ -n "${GOLDEN_FIXTURE_DOWN:-}" ] && bash -c "$GOLDEN_FIXTURE_DOWN" >/dev/null 2>&1

# a recording of nothing is the mistake this guards against
bad=$(grep -lE '^(exit: 12[67])$|command not found|No such file or directory|Permission denied' "$out"/*.txt 2>/dev/null; for f in "$out"/*.txt; do [ "$(grep -vc '^exit: ' "$f")" -eq 0 ] && echo "$f"; done)
if [ -n "$bad" ] && [ "$mode" = record ]; then
  echo "golden-output: refusing to record: these outputs are empty or say the program could not run:"; echo "$bad" | sort -u | sed "s#^$out#    #"
  echo "golden-output: nothing was changed in $golden/"; rm -rf "$out"
  exit 2
fi

if [ "$mode" = record ]; then
  rm -rf "$golden"; mkdir -p "$(dirname "$golden")"; mv "$out" "$golden"
  echo "recorded $(ls "$golden" | wc -l) commands in $golden/ (now read the diff: git diff $golden)"
else
  if diff -r "$golden" "$out"; then echo "identical: $(ls "$out" | wc -l) commands print exactly what they printed when recorded"; rm -rf "$out"
  else echo "DIFFERENT: see above (the new output is in $out)"; exit 1; fi
fi
