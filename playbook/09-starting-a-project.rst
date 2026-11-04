Starting a project
==================

This is the order of work for a project that has not been through this yet, in any language. It assumes an agent following ``kit/AGENT-INSTRUCTIONS.rst``.

Day one
-------

1. Create the repository's working files: ``AGENTS`` (rules), ``docs/backlog`` (the plan), ``docs/development-log`` (newest first, dated from the clock).
2. Set the rules of history: squash merges only; pull request titles are Conventional Commits and are linted.
3. Write the **fast gate** and make it pass on the current project (``kit/scripts/gate.sh`` is a skeleton).
4. Write the **shipper** (``kit/scripts/ship.py``). Check it with ``--check`` against a real token and repository.
5. Make CI run what the gate runs, with a timeout on every job, and measure it once (``kit/scripts/ci-timings.py``) so there is a baseline.
6. Run the **structure metrics** once against the first commit you will compare with, and keep that number.
7. Generate the **outline** and write 15 to 25 real questions for the **findability test**. Expect the first run to be poor: that is the baseline, and it is the work.
8. Write the **idea page**, with an honest "how close are we" section. Link it from the README.

The first ten iterations
------------------------

Do these in roughly this order; each is an iteration (a branch, a pull request).

1. Make every module's first sentence say what it is for, in plain words (the cheapest big win, and what the findability test measures).
2. Rename folders and modules to say what the program is for.
3. Make one command a *story of named steps* as a worked example, and keep it as the model.
4. Add the first architecture guards that the code already satisfies (file size, no prints outside the output module). Then ones it does not, into the ratchet.
5. Run a seeded cold read; fix what it finds; guard the ones that can return.
6. Run the scans (repeated code, bare booleans). Fix the real ones.
7. Add golden output for the commands, on a real fixture.
8. Retire the worst wrong word, with a lexer-based rename and a guard.
9. Use the program as a newcomer. Fix the wording.
10. Measure the CI; fix the largest step; write down what you rejected.

Then continue the loop. When a method stops returning anything new, say so.

Mapping to a language
---------------------

The mechanisms are language-neutral; these are the language-specific parts.

Rust
    First doc sentence: ``//!`` at the top of a file. Guards: an integration test reading ``src/**/*.rs``; a lexer (the ``proc-macro2`` or ``syn`` crates, or a hand-written one) for
    identifier checks. Ratchet and outline: ``kit/guards`` (Python) or a Rust port. Lint: ``clippy`` with warnings denied. CI cache: ``Swatinem/rust-cache``.
Python
    First doc sentence: the module docstring. Guards: ``pytest`` tests reading ``src/**/*.py`` and using the ``ast`` module. Retired words: ``ast`` or ``tokenize`` (a lexer). Lint: ``ruff``.
TypeScript
    First doc sentence: the leading TSDoc comment. Guards: ``vitest`` tests with the TypeScript compiler API or ``ts-morph``; module boundaries with ``dependency-cruiser``.
Go
    First doc sentence: the package comment and each file's leading comment. Guards: ``go test`` with ``go/parser`` and ``go/ast``; ``go vet`` custom analyses.
Any language
    The ratchet, the outline ranking, the scans, the shipper, the gate and the CI report need no language support.

What to expect
--------------

The first week the project gets measurably clearer and the log fills with defects found by reading and scans. The rate of findings does not fall quickly: what changes is their kind, from
stale words and copied rules to *a distinction the code makes and does not name*. After the structural plan empties, the most valuable work is using the program as a newcomer, and then a second
project, which is the honest test of the playbook.

Do not expect to finish. The aim is not a state but a direction, and a record that anyone (or any agent) can pick up.
