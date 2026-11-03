.. Generated from data/ by .tad/tools/render.py. Do not edit by hand.

Session Log
===========

.. _the-idea-found:

The idea: every layer is the top of the layers beneath it
---------------------------------------------------------

Entry date
    2026-10-29

Done
    Rebuilt the core as folders named for what the program is for, wrote one command as a worked example of the idea, and made the commands read as stories of named steps.

Considered
    Layering the core by technical role (ports, adapters, services), which is the usual hexagonal layout.

Rejected
    Folders named for patterns: they explain the architecture, not the program, and a newcomer learns nothing about what the program is for.

----


.. _measure-the-goal-and-automate:

Measure the real goal, and automate the loop
--------------------------------------------

Entry date
    2026-10-29

Done
    Stopped judging progress by impressions: a structure-metrics script compared the code with each earlier release, and the first guards (a file is short enough to read whole, no print outside the presenter) were written as tests. The shipper and the fast gate were built the second time a step was done by hand.

Considered
    A line-count budget as the only measure.

Rejected
    Line counts alone: they are gamed by splitting a file without making it clearer, which is why the stranger test exists beside them.

----


.. _guards-and-ratchets:

Rules found by reading become guards; debts become data
-------------------------------------------------------

Entry date
    2026-11-02

Done
    Each defect found by a read (a sentence written twice, a rule copied by hand, a boolean that was a noun) became a test that reads the source. Rules the code could not yet meet were recorded per file in a data file that may only shrink, so a debt is a list and progress cannot slip back. The last debts were paid the same day.

Considered
    A linter configuration for every rule.

Rejected
    A lint rule cannot read the generated outline, compare a document with the code, or ask the project a question; an ordinary test can.

----


.. _the-rename-incident:

The retired word, seventy-nine times, and a rename that lied
------------------------------------------------------------

Entry date
    2026-11-02

Done
    Renamed 79 uses of a wrong word. Two regex attempts changed a JSON key and a fake tool's raw-string output without any test noticing; a lexer-based renamer that follows string interpolation and verifies that no string literal changed left all 65 hunks right, and a guard now keeps the word out of identifiers.

Considered
    Checking the diff by eye.

Rejected
    Eyes miss a one-character change in a long string; the property to check is that no literal changed, so the tool checks that.

----


.. _text-file-busy:

Main's CI failed on the race I had measured away
------------------------------------------------

Entry date
    2026-11-02

Done
    A test spawned scripts it had just written and CI hit text-file-busy. Put every spawn and every script write behind one lock; a stress test with 16 threads and 4 CPU burners failed 120 of 120 runs before and 0 of 120 after. Wrote down that 740 clean runs on a fast machine are weak evidence against a rare race.

Considered
    Retrying a failed spawn.

Rejected
    A retry hides real contention and teaches the tests nothing; marking the test flaky would have buried the cause.

----


.. _ci-measured-then-optimised:

CI, measured first, then optimised
----------------------------------

Entry date
    2026-11-02

Done
    Baseline over eight runs: median 193 seconds wall and 20.0 job-minutes. The audit step alone compiled its own tool for 181 seconds; a prebuilt cargo-deny, a timeout on every job, cache saved only from main, a job that skips the heavy checks for documents-only changes, and no incremental builds brought a full run to about 177 seconds and 15.7 job-minutes, and a documents-only change to 61 seconds. A speed-up claimed for one job was cherry-picked from the best runs and was retracted in the log when the later releases overlapped.

Considered
    mold as the linker, nextest as the runner, sccache for the Arch build, splitting the Btrfs job, a parallel reproducible build.

Rejected
    mold: lld is already the default linker since Rust 1.90. nextest: a process per test would defeat the in-process lock. The others did not pay in measurement.

----


.. _reads-and-scans:

Seeded reads, and scans for what reading finds one at a time
------------------------------------------------------------

Entry date
    2026-11-03

Done
    Six seeded cold reads each found real issues (stale words, a rule copied in five places, a distinction the code made and never named); a scan for repeated code found them all at once, and a second mode, which forgets names and numbers and compares only shape, found a rule that had been copied and renamed.

Considered
    Reading more modules.

Rejected
    Reading finds one at a time and stops paying once a seed returns what has been read; a scan is cheap and complete.

----


.. _the-idea-page:

Telling the reader the idea
---------------------------

Entry date
    2026-11-03

Done
    Nothing in the repository said in plain words what the code was trying to be. Wrote one page that does: the idea, one request followed from the front door to the machine, how to tell it is healthy, and an honest account of how close each part is to the ideal.

Considered
    Leaving the idea in the canon and a reading list.

Rejected
    A newcomer finds well-organised code with no one telling them why it reads the way it does.

----


.. _reading-by-use:

Using the program as a newcomer would
-------------------------------------

Entry date
    2026-11-03

Done
    Sampling modules stopped finding anything, so the program was run on a real fixture and every word read: a preview that spent two of three numbers on zeros, a first snapshot that never said what its restore point was called, a header showing a retired word. A terminal UI was driven through a pseudo-terminal and its screens printed.

Considered
    More seeded reads.

Rejected
    They returned modules already read; the defects were in what the program says, which only using it shows.

----


.. _the-adapters-were-closer:

A guess written as fact, corrected
----------------------------------

Entry date
    2026-11-03

Done
    The idea page said the adapters were the part least like the ideal. Reading each by its first line showed the opposite. The page was corrected, and the log says that I had guessed and was wrong.

Considered
    Leaving the page as written.

Rejected
    A document that claims how close the code is to the ideal and is not checked against the code is the first thing to rot.

----


.. _release-job-flake:

A release failed on GitHub's own error
--------------------------------------

Entry date
    2026-11-03

Done
    A package-repository job failed with an HTTP 500 while downloading the release's own assets. The failed job was re-run and completed the release; the download script retries five times now.

Considered
    Re-running by hand each time.

Rejected
    That is the repeated hand-work the playbook says to automate.

----


.. _releases-are-batched:

Releases are batched, not one per merge
---------------------------------------

Entry date
    2026-11-03

Done
    A release per merge cost about eight minutes of waiting and gave users a version every few minutes. The release pull request already collects changes, so the shipper stops merging it each time: it releases at ten changes that make a changelog entry, a week of waiting, a change to packaging or the release workflows, or on request. The policy is a small function with ten tested cases, proven to fail when the threshold is off by one.

Considered
    Releasing on a timer; releasing every merge but skipping verification.

Rejected
    A timer releases nothing when nothing changed and everything at once when much did; skipping verification removes the only proof of publishing.

----


.. _hint-ignored-its-switch:

The tip that ignored its own switch
-----------------------------------

Entry date
    2026-11-03

Done
    A hint added a few days earlier did not obey the option that silences hints; found by reading the documentation of the option. It obeys now, and the option says what it governs.

Considered
    Leaving it: it is only one line.

Rejected
    A new thing that lives beside an existing switch has to be wired to it; the switch's own documentation is where the omission shows.

----


.. _the-invented-dates:

The log's dates were invented
-----------------------------

Entry date
    2026-11-03

Done
    While preparing this playbook from the development log, 51 of its 52 headings turned out to carry dates counted forward a day per entry; git said all the work was done in about eight days. They were corrected from git history, the log says so, and the agent notes now say an entry's date is today's date from the clock.

Considered
    Leaving the dates: nothing depended on them.

Rejected
    A record with invented dates cannot be trusted for anything else in it.

----


.. _engine-learns-rst:

The text-as-data engine learns reStructuredText
-----------------------------------------------

Entry date
    2026-11-03

Done
    The renderer builds each page once and writes it through a format object, so Markdown and reStructuredText are one class each; the default is unchanged (byte-identical on the template's real data), the output is validated with docutils with every warning an error, and the renderer, which had no tests, has ten. This repository is the first generated from the template to use it.

Considered
    Converting Markdown to reStructuredText with a separate tool afterwards.

Rejected
    A second tool has two sources of truth; rendering from the data keeps one.
