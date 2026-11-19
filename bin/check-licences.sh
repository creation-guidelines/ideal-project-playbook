#!/bin/sh
# Every tracked file has a licence, and every licence named has its text in the repository: a file is covered
# when a [[annotations]] path (one string or a list) in REUSE.toml matches it (** any depth, * within a folder) or its first 20 lines
# carry SPDX-License-Identifier. The text of MIT is LICENSE-MIT, Apache-2.0 LICENSE-APACHE, CC-BY-SA-4.0
# LICENSE-CC-BY-SA-4.0. Ends 0 when all is covered, 1 when not. Needs git, sed, grep.
set -eu
cd "$(git rev-parse --show-toplevel)"
bad=0
pats=""
if [ -f REUSE.toml ]; then
	pats=$(sed -n 's/^path = //p' REUSE.toml | grep -o '"[^"]*"' | tr -d '"' | sed 's/[.]/\\./g; s/\*\*/\x01/g; s/\*/[^\/]*/g; s/\x01/.*/g; s/^/^/; s/$/$/')
fi
for f in $(git ls-files); do
	ok=0
	for p in $pats; do printf '%s\n' "$f" | grep -Eq "$p" && { ok=1; break; }; done
	[ $ok = 1 ] || { [ -f "$f" ] && head -20 "$f" 2>/dev/null | grep -aq 'SPDX-License-Identifier:'; } && ok=1
	[ $ok = 1 ] || { echo "no licence for $f (REUSE.toml annotation or an SPDX header)"; bad=1; }
done
ids=$({ sed -n 's/^SPDX-License-Identifier = "\(.*\)"$/\1/p' REUSE.toml 2>/dev/null; git grep -ahoE 'SPDX-License-Identifier: [A-Za-z0-9.-]+( (OR|AND) [A-Za-z0-9.-]+)*' -- . ':!bin/check-licences.sh' 2>/dev/null | sed 's/.*Identifier: //'; } | tr ' ' '\n' | grep -vE '^(OR|AND|)$' | sort -u)
for id in $ids; do
	case $id in
	MIT) t=LICENSE-MIT ;; Apache-2.0) t=LICENSE-APACHE ;; CC-BY-SA-4.0) t=LICENSE-CC-BY-SA-4.0 ;;
	*) echo "no known text file for the licence $id (add it to this script)"; bad=1; continue ;;
	esac
	[ -s "$t" ] || { echo "the licence $id has no text: $t"; bad=1; }
done
[ $bad = 0 ] && echo "licences: every tracked file is covered"
exit $bad
