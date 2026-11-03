<!-- Generated from data/ by .tad/tools/render.py. Do not edit by hand. -->

# Backlog

<a id="example-fix-typo"></a>
### EXAMPLE: fix a typo in the intro

Status
: open

Note
: Found while reviewing the first draft.

Opened
: 2026-09-22


<a id="example-add-diagram"></a>
### EXAMPLE: add a diagram to concepts.md

Status
: in-progress

Opened
: 2026-09-22

Relations
: → concerns: [EXAMPLE: one](concepts.md#example-one) — shows a backlog item linked to the concept it is about


<a id="example-license"></a>
### EXAMPLE: choose a license

Status
: done

Note
: Resolved by adding LICENSE.md.

Opened
: 2026-09-22


<a id="subrepo-push-untested"></a>
### git subrepo push has never been exercised

Status
: open

Note
: Only clone/pull have been battle-tested against tad-engine. We never push local .tad/ changes upstream by design, but the command path itself is unverified.

Opened
: 2026-09-22


<a id="pre-pinning-releases-unpinned"></a>
### tad-engine v1.0.0 and v1.0.1 have no dist/vX.Y.Z tag

Status
: open

Note
: The dist-tagging fix only applies going forward; those two releases predate it and stay reachable only via the moving dist branch.

Opened
: 2026-09-22


<a id="render-determinism-untested-multicore"></a>
### render.py determinism has only been verified for dc.py, not render.py itself

Status
: open

Note
: dc.py was stress-tested at 300k rows on a real multi-core GitHub runner; render.py (both the generic one and this repo's custom one) has not had the same treatment.

Opened
: 2026-09-22


<a id="git-subrepo-dependency-risk"></a>
### git-subrepo is a slow-moving third-party dependency

Status
: open

Note
: Last tagged release July 2024 despite ongoing commits, and 201 open issues at last check. A standing risk to monitor, not an active problem.

Opened
: 2026-09-22


<a id="propagate-rfc-style"></a>
### Propagate the RFC-like style to other repos

Status
: done

Note
: Both repos confirmed live: git-rhizoid.github.io pulled the engine cleanly via git subrepo (stock renderer, no conflicts). software-engineering-canon needed the same edit hand-ported to its own local render.py (8 spots) since that file is deliberately not vendored - the pull alone updated only its unused copy of the generic renderer. Both now serve the definition-list style live.

Opened
: 2026-09-22


<a id="render-test-coverage"></a>
### No test coverage for render.py's exact markdown output

Status
: open

Note
: dc.py has a real test suite; render.py does not - the definition-list change was verified with python-markdown's def_list extension as an approximation of kramdown, and against a real Pages build, but nothing catches a future regression automatically.

Opened
: 2026-09-22
