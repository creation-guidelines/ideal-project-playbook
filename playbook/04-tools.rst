Tools
=====

Every tool here was built because something had been done by hand twice. Each is a small script in ``dev/``, documented in
``AGENTS`` and the log, and each does one job so that the loop in ``02-the-loop`` stays cheap. The reference implementations
that are language-neutral are in ``kit/``; the rest are described here so they can be rebuilt for any language.

The gate (``dev/gate.sh``)
--------------------------

*Why:* before every pull request the same seven commands were typed in the same order.

One command runs format, lint, documentation build, link check, licence check, snippet check and tests. Each step writes its own
log to a file and prints one line (``ok  clippy  11s``); a failing step prints the tail of its log. It frees disk when less than
4 GB is free (build directories grow), and ``--full`` adds the slow checks that need a real fixture (golden output, tests on a real
filesystem). It is for reproducing a CI failure and for catching mistakes early. It is not a substitute for the pull request: push, and let
the shipper wait.

The shipper (``kit/scripts/ship.py``)
-------------------------------------

*Why:* an iteration was ten manual steps and a long wait, and the wait did not fit in one tool call.

``ship.py "type: title" --body-file BODY.md`` pushes the current branch, opens the pull request, waits for every check, squash-merges,
waits for the main branch's own CI, decides whether to release (see ``06-ci-and-releases``), and verifies the release. Its rules:

- **It keeps no state.** Every step reads GitHub, so it can be stopped and run again, from any session, and continues from where the
  pull request, main or the release already is.
- **It stops itself before the time limit** of a tool call with exit code 75, *run me again*.
- **It judges a commit by the newest run of each check name**, counts skipped as passing, and reruns a job the runner itself failed to
  start (a runner flake is not a failure of the change).
- It **names a pull request that conflicts** and force-pushes only its own feature branch.
- A documents-only pull request has fewer checks, so the minimum it waits for is configurable.

The token is read from the environment and is never written to a file.

Structure metrics (``kit/scripts/structure-metrics.py``)
--------------------------------------------------------

*Why:* progress was being judged by impression.

It measures the code now against each earlier release tag: number of files, median file, files over a size, files "huddled" just under the
limit, the biggest file, entry files over a size, functions over a size, prints outside the presenter, bare booleans in command signatures,
fields of the window's state, modules with no purpose sentence, purposes in pattern jargon. Run against the tag from the start of the work it
produces the trend in numbers; the plain-word version of that trend is what goes in a report.

The outline and the findability test
-------------------------------------

*Why:* a cold read was the best finder of problems and could not be repeated cheaply.

The outline is generated from each module's first doc sentence. ``kit/guards/outline.py`` does it for Python, Rust, TypeScript, Go and
shell sources. ``kit/guards/findability.py`` ranks it against a list of questions and fails when an answer is not near the top. See
``03-guards``.

Repeated code (``kit/scripts/find-duplicates.py``)
--------------------------------------------------

*Why:* reading finds a rule written twice one module at a time; a scan finds them all at once.

It looks at production code only (tests repeat on purpose), drops comments and blank lines, and reports every run of N identical lines
that appears in more than one place, longest and most repeated first. ``--near`` forgets names, numbers and strings and compares only
the *shape*, which finds a rule that was copied and then renamed to fit. Run on a mature project the near mode is noisy exactly where
regularity is the point (tables, enum-to-word matches); read it for the one real thing and write down why the others are not worth a change.

Seeded reading (``kit/scripts/sample-modules.py``)
--------------------------------------------------

``sample-modules.py SEED N`` picks N random modules per layer. The seed makes a read reproducible, so "I read seed 20261107" is a
checkable statement. When a seed returns modules already read, stop: the method is exhausted.

Tools that rewrite code
-----------------------

These are language-specific (they need a lexer or parser), but the *contract* is not, and it is the part worth copying.

``split-module`` (splits a module by purpose from a small JSON spec)
    Refuses to write unless **every comment is preserved**. It keeps the documentation of the first item after the imports and handles
    modules with no imports. *Lesson:* a defect in the splitter once dropped a comment silently; the verification is what makes it safe
    to use on forty files.

``rename-identifier OLD NEW`` (renames an identifier across the code)
    Built on a **lexer**: it renames identifier tokens only, follows the name inside string interpolation (``{name}``), and afterwards
    verifies that **no string literal changed**; if one did it reverts. *Lesson:* two regex attempts changed a JSON key and a fake tool's raw
    output across 79 renames while every test stayed green. The third, lexer-based, attempt changed none of 65 hunks it was supposed to
    leave alone.

CI timing report (``kit/scripts/ci-timings.py``)
------------------------------------------------

``ci-timings.py --runs 8 --steps`` prints wall time, job-minutes, and the slowest jobs and steps over recent runs of a workflow. It exists
so that every claim about CI speed is a measurement with its samples (``06-ci-and-releases``).

Golden output and fixtures
--------------------------

``golden-output.sh record`` and ``check`` run every command against a real fixture (a script, ``btrfs-fixture.sh up|down``, that builds a small
real filesystem) and store or compare the exact text. Note the pitfall: the script runs the program at a fixed path. From a second working copy
the program was not there, and the recording was *empty*, which showed as 1,096 deleted lines. Read the diff before you commit a recording.

Driving a terminal UI (``kit/scripts/screens.py``)
--------------------------------------------------

In snapall (``dev/tui-e2e.py``), a terminal program is tested through a pseudo-terminal and a terminal emulator library (``pyte``): the test sends keys, waits for text on the
emulated screen, and asserts on it. The same helper, imported without running the suite, is how an agent *looks at* the screens of the program
(``Tui().text()``), which is how the window's prompts and help were read as a newcomer would. (Box-drawing characters are multibyte: do not
cut such output with a byte-oriented tool, or the stream is invalid.)

The catalogue of guards, wired up
---------------------------------

``kit/guards/rules.py`` is the catalogue as functions (each reads files and returns ``{name: number}``, which is exactly what the ratchet takes), and ``kit/guards/architecture.py`` wires them
into one guard with a CONFIG block: this repository's own guard, and the one to copy. A rule is added there when a defect found by a read could return. The retired-word rule uses a small lexer, so a word in a string or a
comment is not mistaken for one in code.

Starting files and CI
---------------------

``kit/templates/`` holds the files a project starts with (agent notes, idea page, log, plan, pull-request body) and ``kit/ci/`` the CI workflow with the measured levers, the pull-request title lint,
the release configuration and a dependency policy. ``kit/README.rst`` is the map.

Release policy as a tested function
-----------------------------------

The decision of when a merge releases is a pure function with ten tested cases (``kit/scripts/test_ship.py``), including the edges and a
mutation check that the test fails when the threshold is off by one. See ``06-ci-and-releases``.

Rebuilding for another language
-------------------------------

What carries over unchanged: the gate, the shipper, the findability ranker, the ratchet, the scans, golden output, the CI report.
What needs the language's own parser: outline extraction (the first doc sentence), the lexer-based rename and split tools, role purity checks.
A useful rule: write the guards in the project's own test framework, so that they run where the other tests run and need no new tool.
