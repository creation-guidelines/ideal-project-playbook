Reading: finding what no guard measures
=======================================

Guards catch what you have already thought of. Reading finds the rest. There are four ways of reading, ordered by cost; use each until it
stops paying, then move to the next.

Seeded cold reads
-----------------

Sample modules at random with a seed, read them *as a stranger*, and write down every place you stumbled. Do not fix while reading;
read the whole sample, then decide.

Six reads on ``snapall`` each found real things. Across them: stale words in messages; a rule copied by hand in five commands (a "way
back" ritual), which became one function used at six sites; a distinction the code made but did not name (a ``bool`` that was really
*Counting::On or Off*, 35 sites in four layers; a ``bool`` that was really *Found::ByTag or ByGuess*); dead plumbing; helpers living in the wrong
module; a sentence told three times.

The rate of findings did not fall across five reads. What changed was the *kind* of finding: from stale words to "a distinction the code
makes and does not name". And then a seed returned four modules already read. That was the signal that sampling was exhausted, and it
is worth treating as an event: write it down and switch method.

Scans
-----

What a read finds one at a time, a scan finds all at once: runs of identical code, runs of code with the same shape, every bare boolean
carried in a pair or a tuple, every hand-spelled plural. A scan also tells you what *not* to fix: the near-duplicate scan on a mature
project is full of tables and enum matches that are meant to look alike, and the log records that and why.

**Search by shape, not by instance.** When you notice ``(AreaName, bool)``, search for every bare bool in a pair, a vector, an option, a return.
When you notice ``snapshot(s)``, search for ``(s)`` and ``(es)`` inside strings (inside strings only: code is full of harmless ``(s)``).

**Read all of the results.** A search for tests that pinned an old wording was cut off after ten lines; ten unrelated matches filled it; the
real-terminal script that pinned the wording never appeared; CI found it. Narrow the pattern until the results are few, or read them all.

Using the program as a newcomer
-------------------------------

When sampling stopped finding anything, the program was run on a real fixture and every word it said was read, in the order a newcomer meets
it: take a first snapshot, list the restore points, change a file, preview going back, go back, undo, read the activity record; then the risky
actions (delete, stop protecting, change limits), then groups, history, room counting, the help, the manual page.

This found things no read of the code had:

- a preview that said *"0 reverted, 1 removed, 0 brought back"*, spending two of three numbers on zeros (worded in four places);
- a first snapshot that never said **what its restore point was called**, the one thing a person needs next;
- a file-history header showing the retired word *config*;
- a health finding that said the same sentence twice;
- command names longer than a fixed help column;
- a sentence correct for many and wrong for exactly one ("delete its 1 snapshots", "taken in 1 areas");
- the singular and the zero ("0 snapshots") in the same places.

A terminal UI is read the same way, through a pseudo-terminal: drive the real program, press the keys, print the screen. Not
everything can be run (a setup conversation for a machine with nothing protected could not, here); then read it the other honest way:
extract every sentence it says, in order, and read them as one conversation.

Read the documentation of every switch
--------------------------------------

Reading the manual page found a defect in the previous day's work: the ``--hints`` option says it shows a one-line tip and that
``--no-hints`` silences it, and a new tip added beside the existing one ignored the option. A new thing that lives next to an existing
switch has to be wired to it, and the switch's own documentation is where an omission shows. Read the help, the manual and the contract as a user would.

When to stop
------------

A method has stopped paying when it returns what you have already seen. Say so, in the log and in the report. Then do one of: change the
method (use the program instead of reading it); change the *project* (a second project, in another language, is the honest test of
whether the playbook transfers); or stop, and say that the structural plan is empty.
