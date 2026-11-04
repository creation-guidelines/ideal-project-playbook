The loop
========

The work is a loop, and the loop is the same at every scale: find something, fix it at the root, guard it,
prove the guard, log it, ship it. This chapter is that loop in detail, and the standing orders that keep an
agent doing it well over a long time.

One iteration
-------------

Each iteration is a **branch from the current** ``origin/main``, **one pull request**, **one squash merge**,
with a conventional title. Branch explicitly::

    git fetch && git checkout -b refactor/what-it-is origin/main

A shell line that failed once skipped its own ``git pull``; the branch lacked recent merges, the pull request
conflicted, got no CI, and the shipper waited on silence. The shipper now names a conflicting pull request, and
force-pushes only its own feature branch.

The steps:

1. **Find.** From a guard that fails, a read, a scan, or a measure that has not moved.
2. **Check the shape.** Do not fix the instance you noticed. Find every place with the same shape and read all of
   the results.
3. **Fix at the root.** Usually this means naming a noun the code uses without naming.
4. **Guard it**, if it could come back.
5. **Prove the guard bites**, once, on purpose.
6. **Check the property**, by running the real program and comparing real output.
7. **Log** what, why, evidence, considered and rejected, mistakes.
8. **Ship**, and release only when the policy says.

Everything in the loop is a file in the repository: the branch and the pull request are the unit; the log and the
plan are documents; nothing lives only in a conversation.

Standing orders
---------------

Decide, do not ask
~~~~~~~~~~~~~~~~~~

An agent given a principle must decide. When two designs are possible, choose by the principle and the project's
interest, and write what was chosen and why in the pull request. Handing the choice back is a failure to do the job.
The exception is a fact only the person has. The journal-weight item on the plan for weeks was dropped by reading
what it would add (the Activity tab already says whether a change can be put back); it was a decision, not a question.

Keep the purpose in sight
~~~~~~~~~~~~~~~~~~~~~~~~~

Long work drifts into busy work. Between iterations ask whether the last action made the project clearer. When a
method stops finding things (a seeded read that returns modules already read), say so and change the method. When
the structural plan is empty, say that, and propose a different kind of check rather than inventing work.

Chain iterations
~~~~~~~~~~~~~~~~

Do several per turn. The shipper is stateless and resumable precisely so that a long wait does not need a human.
When a release is waiting on CI, start the next iteration in a second ``git worktree`` (with a shared build directory)
instead of idling.

State lives in the repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The plan (a table), the log (newest first), the rules (``AGENTS``), and the documentation of every tool are files. An
agent that wakes with no memory reads them and continues. A session that keeps progress only in its own context has
lost it.

Automate the second repetition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The second time a step is done by hand, build the tool, document it, and prefer cheap compute. See ``04-tools``.

Report plainly
~~~~~~~~~~~~~~

The person following the work wants to know how much closer to the ideal it is. They do not want a list of
technical detail. Write what changed, how much closer, what went wrong, and what is next, in plain words. The detail
goes in the pull request and the log, where it belongs. Early reports in this project were too technical and too
long; the instruction to keep them short and plain was given by the person and is now rule.

The ideal as a direction
------------------------

"Ideal, pure, elegant, beautiful" is not a checklist. It is a direction with a test: *can a stranger say what a part
is for from its first line, and be right?* Progress is stated against it, honestly: where the project is close, where it
is not, and what you guessed. A page that says so (the *idea page*) is part of the project and is checked like code.
