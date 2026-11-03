#!/usr/bin/env bash
# One-time bootstrap for a repo freshly generated from this template via GitHub's "Use this
# template" button. Repos generated that way get a single fresh commit with no shared git history
# with text-as-data-template (GitHub does not preserve history or set up a remote for generated
# repos - this is not a fork), so .tad/ arrives as a plain copy, not a git subrepo. This script
# re-adopts it as one, so `git subrepo pull` works from here on. Run it once, right after
# generating the repo, before you've made any other commits that touch .tad/.
#
# Requires git-subrepo (https://github.com/ingydotnet/git-subrepo), a third-party git extension:
#   git clone https://github.com/ingydotnet/git-subrepo /path/to/git-subrepo
#   echo 'source /path/to/git-subrepo/.rc' >> ~/.bashrc   # or add its lib/ dir to PATH
set -euo pipefail
ENGINE_REPO="https://github.com/creation-guidelines/tad-engine.git"
ENGINE_REF="dist"

if [ ! -d .tad ]; then
  echo "No .tad/ directory found - nothing to adopt. Run this from the repo root." >&2
  exit 1
fi

if ! command -v git-subrepo >/dev/null 2>&1 && ! git subrepo version >/dev/null 2>&1; then
  echo "git-subrepo is not installed or not on PATH. See the comment at the top of this script." >&2
  exit 1
fi

if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "Working tree has uncommitted changes. Commit or stash them first." >&2
  exit 1
fi

git rm -rq .tad
git commit -q -m "chore(tad): remove vendored copy before adopting as a git subrepo"
git subrepo clone "$ENGINE_REPO" .tad -b "$ENGINE_REF" -m "chore(tad): vendor engine via git subrepo"
echo "Done. .tad/ is now a git subrepo tracking $ENGINE_REPO ($ENGINE_REF)."
echo "To pull future engine updates: git subrepo pull .tad"
