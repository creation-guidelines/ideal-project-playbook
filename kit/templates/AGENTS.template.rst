AGENTS - how to work in <project>
=================================

This file is for whoever works in this repository, human or agent. Read it first. It is short on purpose: the reasons are in the playbook this project follows
(``kit/AGENT-INSTRUCTIONS.rst`` of ideal-project-playbook), and the history is in the development log.

What this project is for
------------------------

<One sentence a stranger understands: what the program is for, in the words a person would use.>

The aim of the work on it is **clarity**: every layer is the top of the layers beneath it. Each part says what it is for in the words a person uses, and its body uses only
the words of the layer below. A stranger reads a part's first line and can say what it is for, and is right.

Setup (once per session)
------------------------

::

    <the commands that build and test the project, and that bring up any fixture it needs>
    dev/gate.sh          # the fast gate: run before every push
    dev/gate.sh --full   # adds what needs a fixture; CI runs all of it

How an iteration goes
---------------------

1. Branch from the current ``origin/main``: ``git fetch && git checkout -b <type>/<what-it-is> origin/main``.
2. Make the change, and guard it if it could come back: a test that reads the source. What the code cannot yet satisfy goes in ``tests/ratchets.json`` and may only shrink.
3. Prove a new guard bites: break the guarded thing on purpose in a clean file, see it fail, restore the file exactly and compare it.
4. Check the property, not the symptom: run the real program and compare real output (``dev/golden-output.sh check``).
5. Run ``dev/gate.sh``, then ``dev/ship.py "type: title" --body-file BODY.md``. Squash merges only; the title is a Conventional Commit. A release happens when the
   policy says (about ten changes waiting, a week, a change to how releases are published, or ``--release``), not on every merge.
6. **Log** what was done, why, the evidence, what was considered and rejected, and the mistakes, in ``docs/development-log``. The date is today's date from ``date``,
   never counted forward.

Layout
------

<A table: each folder or file, what it is for, who edits it. Folders are named for what the program is for, not for how it is built.>

Rules
-----

- A fact, a word or a rule lives in one place: a sentence a person reads is written once, in the layer that owns it.
- Say what to do next wherever nothing is there or something failed; failures read ``Could not <what>: <why>``; counts are said by one helper (*1 snapshot*, *3 snapshots*,
  *no snapshots*; a length of time keeps its zero).
- A published identity (a key in JSON output, a word stored in an old file) is not renamed for a word: give people a plain word beside it, and write the reason down.
- Hints for a person go to stderr, only to a terminal, and obey the option that silences them. What a script reads from stdout does not change.
- A document that names a path names a real one. A guess is written as a guess. Retract a claim in writing, where you made it.
- Do not claim more than you measured: say how many samples, and say when they overlap.
- Search by the shape of a smell, not the instance you noticed, and read all of the results.
- Do not edit by exact text what a formatter may rewrap; a script that edits several files applies all of its edits or none.

Tools
-----

<One row per tool in dev/: what it does, and the hand-work it removed. Add a row, and a log entry, whenever you build one.>

What "done" means for a change
------------------------------

The gate passes; the real output is unchanged or the change is exactly the intended lines of it; every pin on an old wording was found and updated; a new guard was shown to
fail; the log says what was done and why; CI is green on the newest run of every check.

Reporting
---------

Short and plain, at the big picture: what changed, how much closer to the ideal, what went wrong, what is next. Detail goes in the log and the pull request. If nothing has
been tried on the person's own machine, say so.
