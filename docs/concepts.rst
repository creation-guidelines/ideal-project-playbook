.. Generated from data/ by .tad/tools/render.py. Do not edit by hand.

Concepts
========

.. _top-of-the-layers-beneath:

Every layer is the top of the layers beneath it
-----------------------------------------------

Statement
    Read from the top, each part says what it is *for*, in the words a person uses; each step down says *how*, using only the words of the layer beneath it. You can stop at any level and still understand the program, and you never have to hold all of it in your head. This is the one idea the rest of the playbook serves.

Tags
    principle

Relations
    - ← part-of: `Two faces: what it is for, and a body in the words beneath <concepts.rst#two-faces>`__
    - ← part-of: `Each layer is a small language <concepts.rst#small-languages>`__

Sources
    `software-engineering-canon: the curated reference these practices were taken from <https://github.com/creation-guidelines/software-engineering-canon>`__


.. _two-faces:

Two faces: what it is for, and a body in the words beneath
----------------------------------------------------------

Statement
    Every part has an upward face (its purpose, and the words it offers) and a downward face (a body written only in the words of the layers below). A part that cannot be described that way is doing two jobs, and is split.

Tags
    principle

Relations
    - → part-of: `Every layer is the top of the layers beneath it <concepts.rst#top-of-the-layers-beneath>`__

Sources
    `software-engineering-canon: the curated reference these practices were taken from <https://github.com/creation-guidelines/software-engineering-canon>`__, `snapall development log: what was done, why, the evidence and the mistakes, newest first <https://github.com/grenudi/snapall/blob/main/docs/development-log.md>`__


.. _small-languages:

Each layer is a small language
------------------------------

Statement
    A layer offers a vocabulary (types, verbs, nouns) and the layer above is written in it. A command reads as a story of those words: look, ask, begin, do, end, show. The reader meets the story first and the mechanism only when they ask.

Tags
    principle, structure

Relations
    - → part-of: `Every layer is the top of the layers beneath it <concepts.rst#top-of-the-layers-beneath>`__
    - ← part-of: `Names explain the program <concepts.rst#names-explain>`__

Sources
    `snapall: a Rust command line and terminal UI over snapper, the worked example of everything in this playbook <https://github.com/grenudi/snapall>`__, `software-engineering-canon: the curated reference these practices were taken from <https://github.com/creation-guidelines/software-engineering-canon>`__


.. _names-explain:

Names explain the program
-------------------------

Statement
    Names of files, folders, actions and states say what the thing is for, in plain words. Folders are named for what the program is *for*, not for how it is built (``going_back/``, not ``adapters/``). A part's first sentence says what it is for without a pattern word like adapter or port.

Tags
    structure, clarity

Relations
    - → part-of: `Each layer is a small language <concepts.rst#small-languages>`__

Sources
    `software-engineering-canon: the curated reference these practices were taken from <https://github.com/creation-guidelines/software-engineering-canon>`__, `snapall development log: what was done, why, the evidence and the mistakes, newest first <https://github.com/grenudi/snapall/blob/main/docs/development-log.md>`__


.. _one-fact-one-place:

A fact, a word or a rule lives in one place
-------------------------------------------

Statement
    A sentence a person reads, a plural, a rule about disks, a way of counting: written once, in the layer that owns it, and used everywhere. Every copy is a place it can come out differently. Guards forbid the copy, and a helper makes the one place cheap to use.

Tags
    structure, clarity

Relations
    - → enforced-by: `Guards are tests that read the source <concepts.rst#guards-are-tests>`__ — a copy of a sentence or a rule is a failing test
    - ← needs: `Say what to do next, once <concepts.rst#say-what-to-do-next>`__

Sources
    `snapall development log: what was done, why, the evidence and the mistakes, newest first <https://github.com/grenudi/snapall/blob/main/docs/development-log.md>`__


.. _stranger-test:

The stranger test
-----------------

Statement
    Someone who has never seen the code should be able to say what a part is for from its first line, and be right. It is the measure of clarity, and the only one that cannot be gamed by moving code around.

Tags
    measure, clarity

Relations
    - ← extends: `Findability as a test <concepts.rst#findability-test>`__ — the stranger test, run on every change
    - ← extends: `Seeded cold reads <concepts.rst#seeded-cold-reads>`__

Sources
    `snapall development log: what was done, why, the evidence and the mistakes, newest first <https://github.com/grenudi/snapall/blob/main/docs/development-log.md>`__


.. _findability-test:

Findability as a test
---------------------

Statement
    Generate an outline from every module's first sentence, then ask it real questions in a test ("where is it said which kind of disk we work with?") and fail if the answer is not near the top. A cold read, turned into something that runs on every change. If a description is vague, or a thing is in the wrong place, it shows here first.

Tags
    measure, guard

Relations
    - → extends: `The stranger test <concepts.rst#stranger-test>`__ — the stranger test, run on every change

Sources
    `snapall: a Rust command line and terminal UI over snapper, the worked example of everything in this playbook <https://github.com/grenudi/snapall>`__


.. _guards-are-tests:

Guards are tests that read the source
-------------------------------------

Statement
    Architecture rules are ordinary tests that read the source tree (or its parsed form) and fail naming the file and line. A rule that lives only in a document is a wish; a rule that fails the build is a property of the project.

Tags
    guard

Relations
    - ← enforced-by: `A fact, a word or a rule lives in one place <concepts.rst#one-fact-one-place>`__ — a copy of a sentence or a rule is a failing test
    - ← part-of: `Debts are data and only shrink <concepts.rst#ratchet>`__
    - ← needs: `Prove every guard bites <concepts.rst#prove-the-guard-bites>`__
    - ← part-of: `Pin the real output <concepts.rst#golden-output>`__
    - ← enforced-by: `Retire a word with a guard <concepts.rst#retire-words>`__
    - ← enforced-by: `Documents are checked against the code <concepts.rst#docs-tell-the-truth>`__

Sources
    `snapall: a Rust command line and terminal UI over snapper, the worked example of everything in this playbook <https://github.com/grenudi/snapall>`__


.. _ratchet:

Debts are data and only shrink
------------------------------

Statement
    A rule that cannot be met today is recorded as a number per file in a data file. The test fails if any number grows, and insists the file record any decrease. Progress cannot silently slip back, and what remains is a list anyone can read.

Tags
    guard, measure

Relations
    - → part-of: `Guards are tests that read the source <concepts.rst#guards-are-tests>`__

Sources
    `snapall: a Rust command line and terminal UI over snapper, the worked example of everything in this playbook <https://github.com/grenudi/snapall>`__


.. _prove-the-guard-bites:

Prove every guard bites
-----------------------

Statement
    A guard that has only ever passed is unproven. Break the thing it guards on purpose, in a clean file, confirm it fails with a useful message, then restore the file *exactly* (and compare). Two checks can pass together for the wrong reason, for example a link and its target both wrong in the same way, so test the rule against the outside truth too.

Tags
    guard, discipline

Relations
    - → needs: `Guards are tests that read the source <concepts.rst#guards-are-tests>`__
    - ← extends: `Check the property, not the symptom <concepts.rst#check-the-property>`__

Sources
    `snapall development log: what was done, why, the evidence and the mistakes, newest first <https://github.com/grenudi/snapall/blob/main/docs/development-log.md>`__


.. _check-the-property:

Check the property, not the symptom
-----------------------------------

Statement
    A compile, a green build or a passing test is not the check that a change did what you meant. Check the property itself: that no string literal changed under a rename, that the output is byte-identical, that the real program says what you think it says. Almost every surprise in this project was a symptom taken for the property.

Tags
    discipline

Relations
    - → extends: `Prove every guard bites <concepts.rst#prove-the-guard-bites>`__
    - ← extends: `Tools that rewrite code verify themselves <concepts.rst#tools-verify-themselves>`__
    - ← needs: `Remove a race by construction <concepts.rst#race-by-construction>`__
    - ← needs: `Search by shape, and read all of the results <concepts.rst#search-by-shape>`__
    - ← extends: `Generalise a tool with a parity test <concepts.rst#generalise-with-a-parity-test>`__ — the property is: it still does what the original did

Sources
    `snapall development log: what was done, why, the evidence and the mistakes, newest first <https://github.com/grenudi/snapall/blob/main/docs/development-log.md>`__


.. _measure-before-and-after:

Measure before you claim
------------------------

Statement
    Say how long, how many, how big, before and after, with the samples, and say when the samples overlap. A claim chosen from the best runs is not a measurement. When you find you overclaimed, retract it in writing, where the claim was made.

Tags
    discipline, measure

Relations
    - ← needs: `Measure the CI before optimising it <concepts.rst#measure-the-ci-first>`__

Sources
    `snapall development log: what was done, why, the evidence and the mistakes, newest first <https://github.com/grenudi/snapall/blob/main/docs/development-log.md>`__


.. _seeded-cold-reads:

Seeded cold reads
-----------------

Statement
    Pick modules at random with a seed (so the read is reproducible), read them as a stranger, and write down where you stumbled. It finds what no guard measures: a rule copied by hand, a stale word, a distinction the code makes and never names. It stops paying when a seed returns modules you have already read; that is the signal to read differently.

Tags
    measure, reading

Relations
    - → extends: `The stranger test <concepts.rst#stranger-test>`__
    - ← extends: `Use the program as a newcomer would <concepts.rst#use-it-as-a-newcomer>`__ — when reading code stops finding things

Sources
    `snapall: a Rust command line and terminal UI over snapper, the worked example of everything in this playbook <https://github.com/grenudi/snapall>`__


.. _use-it-as-a-newcomer:

Use the program as a newcomer would
-----------------------------------

Statement
    Run the real program on a real disk, from first use to going back, and read every word it says; drive a terminal UI through a pseudo-terminal and print its screens. Reading code finds what is wrong with code; only using the program finds what is wrong with what it *says*.

Tags
    reading, clarity

Relations
    - → extends: `Seeded cold reads <concepts.rst#seeded-cold-reads>`__ — when reading code stops finding things
    - ← extends: `Look at what people will see <concepts.rst#look-at-what-people-see>`__ — for what is seen rather than read

Sources
    `snapall: a Rust command line and terminal UI over snapper, the worked example of everything in this playbook <https://github.com/grenudi/snapall>`__


.. _golden-output:

Pin the real output
-------------------

Statement
    Record the exact text of the program's commands on a real fixture, and fail CI when it differs. A change to wording then shows as the few lines that moved, reviewed as such. Re-record only after reading the diff: a recording of empty output looks as clean as a good one until you read it.

Tags
    guard, output

Relations
    - → part-of: `Guards are tests that read the source <concepts.rst#guards-are-tests>`__

Sources
    `snapall development log: what was done, why, the evidence and the mistakes, newest first <https://github.com/grenudi/snapall/blob/main/docs/development-log.md>`__


.. _tools-verify-themselves:

Tools that rewrite code verify themselves
-----------------------------------------

Statement
    A splitter, a renamer or a formatter that edits many files checks its own work: every comment survives, no string literal changed, nothing is written unless everything matches. A regex rename once changed a JSON key and a fake tool's output; a lexer-based one that verifies the strings changed none.

Tags
    automation, discipline

Relations
    - → extends: `Check the property, not the symptom <concepts.rst#check-the-property>`__
    - ← needs: `Retire a word with a guard <concepts.rst#retire-words>`__
    - ← needs: `Generalise a tool with a parity test <concepts.rst#generalise-with-a-parity-test>`__

Sources
    `snapall: a Rust command line and terminal UI over snapper, the worked example of everything in this playbook <https://github.com/grenudi/snapall>`__


.. _automate-repeated-hand-work:

Automate what you do twice by hand
----------------------------------

Statement
    The second time a manual step is repeated, build the tool, document it in the repository's agent notes and log, and use cheap compute (CI) where it can. The ship script, the gate, the splitter, the scans and the timing report each began as a step done by hand twice.

Tags
    automation

Relations
    - → needs: `State and plans live in the repository <concepts.rst#state-in-the-repo>`__ — the tool is documented in the repository, or the next agent rebuilds it
    - ← part-of: `A stateless, resumable shipper <concepts.rst#resumable-shipper>`__
    - ← part-of: `A fast local gate; CI for the rest <concepts.rst#fast-gate>`__

Sources
    `snapall development log: what was done, why, the evidence and the mistakes, newest first <https://github.com/grenudi/snapall/blob/main/docs/development-log.md>`__


.. _state-in-the-repo:

State and plans live in the repository
--------------------------------------

Statement
    An agent's memory is not the project's memory. The plan (backlog), the decisions (log), the rules (agent notes) and the documentation of the tools are files in the repository, so no session starts over and any agent can continue where another stopped.

Tags
    process

Relations
    - ← needs: `Automate what you do twice by hand <concepts.rst#automate-repeated-hand-work>`__ — the tool is documented in the repository, or the next agent rebuilds it
    - ← needs: `One branch, one merged pull request per iteration <concepts.rst#branch-per-iteration>`__

Sources
    `tad-engine: the text-as-data engine this repository is built on <https://github.com/creation-guidelines/tad-engine>`__, `git-subrepo: vendor another repository as a folder, and pull updates into it <https://github.com/ingydotnet/git-subrepo>`__


.. _branch-per-iteration:

One branch, one merged pull request per iteration
-------------------------------------------------

Statement
    Each iteration is a branch from the current main, a pull request whose body says what and why and shows the evidence, and a squash merge with a conventional title. History reads as the story of the work, and nothing depends on a conversation.

Tags
    process

Relations
    - → needs: `State and plans live in the repository <concepts.rst#state-in-the-repo>`__
    - ← needs: `A stateless, resumable shipper <concepts.rst#resumable-shipper>`__

Sources
    `Conventional Commits 1.0.0 <https://www.conventionalcommits.org/>`__


.. _resumable-shipper:

A stateless, resumable shipper
------------------------------

Statement
    One script pushes, opens the pull request, waits for checks, merges and verifies. It keeps no state of its own, reading GitHub every time, and it stops itself before the tool's time limit with a code that means *run me again*. Any session can continue what another began.

Tags
    automation, process

Relations
    - → part-of: `Automate what you do twice by hand <concepts.rst#automate-repeated-hand-work>`__
    - → needs: `One branch, one merged pull request per iteration <concepts.rst#branch-per-iteration>`__
    - ← part-of: `Judge CI by the newest run of each check <concepts.rst#newest-run-counts>`__

Sources
    `snapall: a Rust command line and terminal UI over snapper, the worked example of everything in this playbook <https://github.com/grenudi/snapall>`__


.. _fast-gate:

A fast local gate; CI for the rest
----------------------------------

Statement
    One command runs what must pass before shipping (format, lint, docs, links, licences, tests), writes each step's log to a file and prints one line per step. CI runs the heavy matrix. The gate is for reproducing a failure and for catching mistakes early, not a substitute for the pull request.

Tags
    automation, process

Relations
    - → part-of: `Automate what you do twice by hand <concepts.rst#automate-repeated-hand-work>`__

Sources
    `snapall: a Rust command line and terminal UI over snapper, the worked example of everything in this playbook <https://github.com/grenudi/snapall>`__


.. _newest-run-counts:

Judge CI by the newest run of each check
----------------------------------------

Statement
    Reruns and flakes leave old failures in the history. Judge a commit by the newest run of each check name, count skipped as passing, and rerun a job the runner itself failed to start. A release is the commit titled as one, not the merge before it.

Tags
    process, ci

Relations
    - → part-of: `A stateless, resumable shipper <concepts.rst#resumable-shipper>`__

Sources
    `snapall development log: what was done, why, the evidence and the mistakes, newest first <https://github.com/grenudi/snapall/blob/main/docs/development-log.md>`__


.. _measure-the-ci-first:

Measure the CI before optimising it
-----------------------------------

Statement
    Collect wall time, job-minutes and the slowest jobs and steps over several runs, then change the critical path. The biggest win here was one step, a security audit that compiled its own tool for three minutes. Reject, with reasons, what the measurement does not support.

Tags
    ci, measure

Relations
    - → needs: `Measure before you claim <concepts.rst#measure-before-and-after>`__
    - ← extends: `The levers that paid <concepts.rst#ci-small-levers>`__
    - ← extends: `Release in batches, not on every merge <concepts.rst#batch-releases>`__

Sources
    `snapall development log: what was done, why, the evidence and the mistakes, newest first <https://github.com/grenudi/snapall/blob/main/docs/development-log.md>`__


.. _ci-small-levers:

The levers that paid
--------------------

Statement
    A prebuilt tool instead of compiling it; a timeout on every job; the cache saved only from main; narrower triggers so a documents-only change skips the heavy jobs; no incremental builds or full debug info in CI; retries on the network. A policy swap (here, the audit's rules) was proven locally against a known-bad case before it replaced the old one.

Tags
    ci

Relations
    - → extends: `Measure the CI before optimising it <concepts.rst#measure-the-ci-first>`__

Sources
    `snapall: a Rust command line and terminal UI over snapper, the worked example of everything in this playbook <https://github.com/grenudi/snapall>`__, `cargo-deny: lint the dependency graph (advisories, licences, bans) <https://github.com/EmbarkStudios/cargo-deny>`__, `Swatinem/rust-cache: cache Rust build artefacts in GitHub Actions <https://github.com/Swatinem/rust-cache>`__


.. _batch-releases:

Release in batches, not on every merge
--------------------------------------

Statement
    A release per merge costs minutes of waiting and gives users a new version every few minutes, while proving little that CI does not. Release when about ten changes wait, or the oldest has waited a week, or a change touches how releases are *published* (the one thing only a release proves), or on request. Make the policy a small tested function.

Tags
    ci, process

Relations
    - → extends: `Measure the CI before optimising it <concepts.rst#measure-the-ci-first>`__

Sources
    `snapall: a Rust command line and terminal UI over snapper, the worked example of everything in this playbook <https://github.com/grenudi/snapall>`__, `release-plz: release pull requests and changelogs from conventional commits <https://release-plz.dev/>`__


.. _race-by-construction:

Remove a race by construction
-----------------------------

Statement
    A rare failure is not disproved by many clean runs on a fast machine. Find the shared resource, put every use behind one lock, and show with a stress test that the original fails and the fixed version does not.

Tags
    discipline, ci

Relations
    - → needs: `Check the property, not the symptom <concepts.rst#check-the-property>`__

Sources
    `snapall development log: what was done, why, the evidence and the mistakes, newest first <https://github.com/grenudi/snapall/blob/main/docs/development-log.md>`__


.. _retire-words:

Retire a word with a guard
--------------------------

Statement
    When a word is wrong (here, *config* for an area), rename its uses with a lexer-based tool that follows string interpolation and verifies no literal changed, then add a guard that the word is not an identifier outside the adapter that owns it.

Tags
    clarity, guard

Relations
    - → needs: `Tools that rewrite code verify themselves <concepts.rst#tools-verify-themselves>`__
    - → enforced-by: `Guards are tests that read the source <concepts.rst#guards-are-tests>`__
    - ← extends: `Published identities are not renamed for a word <concepts.rst#published-names-stay>`__ — the exception that is written down

Sources
    `snapall development log: what was done, why, the evidence and the mistakes, newest first <https://github.com/grenudi/snapall/blob/main/docs/development-log.md>`__


.. _published-names-stay:

Published identities are not renamed for a word
-----------------------------------------------

Statement
    A key in a JSON output, a contract's identity, a stored word in a journal: other programs and older files read them. Give people a plain word beside the stored one, test both, and leave the stored one alone, with the reason written down.

Tags
    clarity, discipline

Relations
    - → extends: `Retire a word with a guard <concepts.rst#retire-words>`__ — the exception that is written down

Sources
    `snapall development log: what was done, why, the evidence and the mistakes, newest first <https://github.com/grenudi/snapall/blob/main/docs/development-log.md>`__


.. _docs-tell-the-truth:

Documents are checked against the code
--------------------------------------

Statement
    A document that names a path is checked to name a real one; a code example in a document is compared with the source; a page about how close the code is to the ideal says where it is not close. A guess written as fact is corrected in writing when it turns out wrong, and so is an invented date.

Tags
    guard, clarity

Relations
    - → enforced-by: `Guards are tests that read the source <concepts.rst#guards-are-tests>`__

Sources
    `reStructuredText: the markup specification and docutils <https://docutils.sourceforge.io/rst.html>`__


.. _plain-reports:

Report in plain words, at the big picture
-----------------------------------------

Statement
    Say what changed, how much closer it is to the ideal, what went wrong, and what is next, in language a person who does not read the code can follow. Technical detail belongs in the log and the pull request. Own mistakes briefly and say what they taught.

Tags
    process, communication

Relations
    - ← needs: `Decide, following the canon and the project's interest <concepts.rst#decide-yourself>`__

Sources
    `snapall development log: what was done, why, the evidence and the mistakes, newest first <https://github.com/grenudi/snapall/blob/main/docs/development-log.md>`__


.. _decide-yourself:

Decide, following the canon and the project's interest
------------------------------------------------------

Statement
    An agent given a principle decides, and says what it decided and why, instead of handing the choice back. It asks only when the answer needs something it cannot know, and it checks between iterations that each action still serves the purpose and is not busy work.

Tags
    process, communication

Relations
    - → needs: `Report in plain words, at the big picture <concepts.rst#plain-reports>`__

Sources
    `snapall development log: what was done, why, the evidence and the mistakes, newest first <https://github.com/grenudi/snapall/blob/main/docs/development-log.md>`__


.. _search-by-shape:

Search by shape, and read all of the results
--------------------------------------------

Statement
    To find a smell, search by its *shape* (every bare bool in a pair, every ``if n == 1``), not by the instance you noticed. Read the whole result: a search cut off after ten lines once hid the one script that pinned a change, and CI found it.

Tags
    reading, discipline

Relations
    - → needs: `Check the property, not the symptom <concepts.rst#check-the-property>`__

Sources
    `snapall development log: what was done, why, the evidence and the mistakes, newest first <https://github.com/grenudi/snapall/blob/main/docs/development-log.md>`__


.. _say-what-to-do-next:

Say what to do next, once
-------------------------

Statement
    Every situation where nothing is there, or something failed, says what to do about it, in the layer that owns the words, so every surface (command line, window) is equally helpful and none repeats it differently.

Tags
    clarity, output

Relations
    - → needs: `A fact, a word or a rule lives in one place <concepts.rst#one-fact-one-place>`__

Sources
    `snapall development log: what was done, why, the evidence and the mistakes, newest first <https://github.com/grenudi/snapall/blob/main/docs/development-log.md>`__


.. _generalise-with-a-parity-test:

Generalise a tool with a parity test
------------------------------------

Statement
    When a script built for one project is made general, run the general one and the original on the original's own project and compare the results. If they differ, form a hypothesis and test it with a controlled experiment (give the new one the old one's exact rule and see whether the results then match) until every difference is explained and deliberate. A generalisation that is 'about the same' has changed something nobody chose.

Tags
    discipline, automation

Relations
    - → extends: `Check the property, not the symptom <concepts.rst#check-the-property>`__ — the property is: it still does what the original did
    - → needs: `Tools that rewrite code verify themselves <concepts.rst#tools-verify-themselves>`__

Sources
    `snapall: a Rust command line and terminal UI over snapper, the worked example of everything in this playbook <https://github.com/grenudi/snapall>`__


.. _look-at-what-people-see:

Look at what people will see
----------------------------

Statement
    A check that a page answers, or that every link on it resolves, cannot see that it looks wrong. Look at it the way a reader will: a screenshot of the real page in a real browser, of the live site and not only of a local build. Three defects of this playbook's own site (literals not styled as code, a table of contents drawn like the navigation bar, headings drawn as links) were visible only that way.

Tags
    reading, output

Relations
    - → extends: `Use the program as a newcomer would <concepts.rst#use-it-as-a-newcomer>`__ — for what is seen rather than read

Sources
    `This playbook's lessons chapter: each mistake, and the rule it became <https://github.com/creation-guidelines/ideal-project-playbook/blob/main/playbook/08-lessons.rst>`__


.. _look-around-first:

Look around first
-----------------

Statement
    Before acting, take a clear look at the situation: what is, what we are dealing with, why it is so, and what others already learned. Keep what was found as research - the question, the findings, their sources - so the decisions that rest on it can cite it, and anyone can follow a step down to what it stands on.

Tags
    practice, research

Sources
    `The OODA loop: observe, orient, decide, act <https://en.wikipedia.org/wiki/OODA_loop>`__, `The Thing: Why I Am a Catholic (the fence) <https://en.wikipedia.org/wiki/G._K._Chesterton#Chesterton's_fence>`__, `The Toyota Way (go and see) <https://en.wikipedia.org/wiki/Genchi_Genbutsu>`__
