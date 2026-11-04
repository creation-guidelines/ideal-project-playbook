Guards
======

A **guard** is an ordinary test that reads the source tree (or its parsed form) and fails, naming the file and line,
when a rule is broken. A rule that lives only in a document is a wish. A rule that fails the build is a property of the
project.

Why tests and not a linter
--------------------------

A linter rule sees one file. The rules that matter most here compare things: a document with the code, a generated
outline with a list of questions, a sentence in one layer with a sentence in another. Only an ordinary test, in the
project's own language, can read the outline, open a document, and ask the project a question.

Debts as data: the ratchet
--------------------------

Most rules cannot be satisfied on the day you write them. The ratchet makes that safe.

For each rule, the test computes a number per file (how many lines over, how many copies, how many hand-spelled
plurals). The numbers are stored in a data file, ``tests/ratchets.json``. The test fails if:

- any number is **higher** than recorded (a new debt), or
- any number is **lower** and the file was not updated (progress must be written down).

``UPDATE_RATCHETS=1`` rewrites the file. The effect is that progress cannot slip back, and the remaining debt is a list
anyone can read. In ``snapall`` the whole debt, at the end of the work described here, was a single entry: the one table of
every flag, 498 lines, a table that is long because the thing it lists is long.

Proving a guard bites
---------------------

A guard that has only ever passed is unproven. After writing one:

1. In a **clean file**, add exactly the thing the guard forbids (and, in the same edit, one innocent look-alike that it
   must not flag).
2. Run the guard. It must fail, naming the file, and must count the forbidden thing and only that.
3. Restore the file **exactly**, and *compare* it with a copy taken before.
4. Run the guard again: it passes.

Two checks can pass for the same wrong reason. When the link-target test and the link generator both used the same wrong
function for an identifier, the targets matched the links and everything was green; only a test that compared the rule with
what the outside tool (docutils) actually does failed. Always include one check against the outside truth.

The catalogue
-------------

These grew one at a time, each from a defect that a read found.

Size and shape
~~~~~~~~~~~~~~

- A file is short enough to read whole (the long ones are in the ratchet).
- Entry files stay short.
- No two modules share a purpose sentence.
- No module's first sentence uses a pattern word where a plain one would do.

Purity by role
~~~~~~~~~~~~~~

Decide the *role* of a file by its name, then enforce what each role may touch. Only files that are drawing may use the
drawing library. Only the output module prints. Only the adapters know where things live on the machine. The core asking the
machine whether a file exists at a Linux path was a defect found by a read; the core now asks the question it actually means
("is the boot-menu plugin installed?") and the adapter owns the path.

One place
~~~~~~~~~

- No run of four lines of production code appears in two places.
- A sentence about a requirement is told in one place.
- A plural is said by a helper and never spelled by hand. The idiom ``if n == 1 { "" } else { "s" }`` in any words is caught,
  and so is ``snapshot(s)``, which is the other way of not saying it. *No snapshots*, not *0 snapshots*.
- A sentence a person reads in two layers is one function in the core.

Vocabulary
~~~~~~~~~~

A retired word is not an identifier outside the one adapter that owns it. This is checked by a **lexer**, not a regex: a regex
rename and a regex guard both mistake a word in a string for a word in code.

Documents tell the truth
~~~~~~~~~~~~~~~~~~~~~~~~

A document that names a path names a real one; a code example in a document equals the source; the idea page says where the code
is not close to the ideal.

Findability: the cold read as a test
------------------------------------

Generate an **outline** of the whole program from every module's first sentence (its purpose). Write a list of real questions a
newcomer would ask ("where is it said which kind of disk we work with?", "where does a restore point get put back?"), each with the
module that should answer it. A test ranks the outline against each question (lowercase, split into words, strip common endings, a
short table of irregular forms) and fails when the right module is not near the top.

In ``snapall`` there are 52 questions; all 52 answers are within the first three results and about 37 are first. The outline is regenerated
on a change and the diff is reviewed: if a sentence became vague, a question drops in rank and the test says which.

This is the stranger test made mechanical. It is cheap, deterministic, and it catches a description that no longer says what the part is
for, which no other guard can.

Golden output
~~~~~~~~~~~~~

Record the exact text of every command on a real fixture (a small real disk or service brought up by a script). Fail CI when any
output differs. A change to wording then shows as the few lines that moved, and is reviewed as such.

Two cautions, both learned the hard way. Re-record only after *reading the diff*: a recording made when the program could not be found
once showed 1,096 deleted lines across twenty files, which looks like a clean change until you read it. And compare the output of a
command that prints its own timestamp with that field removed, or it differs on every run.

Where the guards live
---------------------

In ``snapall`` they are an ``architecture`` test file (31 tests), the ``findability`` test with its question list, the ratchet file, a
``golden`` script, and structure metrics that compare the code with any earlier release. ``kit/guards`` has a language-neutral
implementation of the ratchet, the outline and the findability ranking, with tests, which any project can start from.
