<!-- Generated from data/ by tad. Do not edit by hand. -->

# Concepts

<a id="top-of-the-layers-beneath"></a>
### Every layer is the top of the layers beneath it

Summary
: Read from the top, each part says what it is *for*, in the words a person uses; each step down says *how*, using only the words of the layer beneath it. You can stop at any level and still understand the program, and you never have to hold all of it in your head. This is the one idea the rest of the playbook serves.

Tags
: principle

Relations
: ← part-of: [Two faces: what it is for, and a body in the words beneath](concepts.md#two-faces)
: ← part-of: [Each layer is a small language](concepts.md#small-languages)

Sources
: [software-engineering-canon: the curated reference these practices were taken from](https://github.com/creation-guidelines/software-engineering-canon)


<a id="two-faces"></a>
### Two faces: what it is for, and a body in the words beneath

Summary
: Every part has an upward face (its purpose, and the words it offers) and a downward face (a body written only in the words of the layers below). A part that cannot be described that way is doing two jobs, and is split.

Tags
: principle

Relations
: → part-of: [Every layer is the top of the layers beneath it](concepts.md#top-of-the-layers-beneath)

Sources
: [software-engineering-canon: the curated reference these practices were taken from](https://github.com/creation-guidelines/software-engineering-canon), [snapall development log: what was done, why, the evidence and the mistakes, newest first](https://github.com/grenudi/snapall/blob/main/docs/development-log.md)


<a id="small-languages"></a>
### Each layer is a small language

Summary
: A layer offers a vocabulary (types, verbs, nouns) and the layer above is written in it. A command reads as a story of those words: look, ask, begin, do, end, show. The reader meets the story first and the mechanism only when they ask.

Tags
: principle, structure

Relations
: → part-of: [Every layer is the top of the layers beneath it](concepts.md#top-of-the-layers-beneath)
: ← part-of: [Names explain the program](concepts.md#names-explain)

Sources
: [snapall: a Rust command line and terminal UI over snapper, the worked example of everything in this playbook](https://github.com/grenudi/snapall), [software-engineering-canon: the curated reference these practices were taken from](https://github.com/creation-guidelines/software-engineering-canon)


<a id="names-explain"></a>
### Names explain the program

Summary
: Names of files, folders, actions and states say what the thing is for, in plain words. Folders are named for what the program is *for*, not for how it is built (`going_back/`, not `adapters/`). A part's first sentence says what it is for without a pattern word like adapter or port.

Tags
: structure, clarity

Relations
: → part-of: [Each layer is a small language](concepts.md#small-languages)

Sources
: [software-engineering-canon: the curated reference these practices were taken from](https://github.com/creation-guidelines/software-engineering-canon), [snapall development log: what was done, why, the evidence and the mistakes, newest first](https://github.com/grenudi/snapall/blob/main/docs/development-log.md)


<a id="one-fact-one-place"></a>
### A fact, a word or a rule lives in one place

Summary
: A sentence a person reads, a plural, a rule about disks, a way of counting: written once, in the layer that owns it, and used everywhere. Every copy is a place it can come out differently. Guards forbid the copy, and a helper makes the one place cheap to use.

Tags
: structure, clarity

Relations
: → enforced-by: [Guards are tests that read the source](concepts.md#guards-are-tests) — a copy of a sentence or a rule is a failing test
: ← needs: [Say what to do next, once](concepts.md#say-what-to-do-next)

Sources
: [snapall development log: what was done, why, the evidence and the mistakes, newest first](https://github.com/grenudi/snapall/blob/main/docs/development-log.md)


<a id="stranger-test"></a>
### The stranger test

Summary
: Someone who has never seen the code should be able to say what a part is for from its first line, and be right. It is the measure of clarity, and the only one that cannot be gamed by moving code around.

Tags
: measure, clarity

Relations
: ← extends: [Findability as a test](concepts.md#findability-test) — the stranger test, run on every change
: ← extends: [Seeded cold reads](concepts.md#seeded-cold-reads)

Sources
: [snapall development log: what was done, why, the evidence and the mistakes, newest first](https://github.com/grenudi/snapall/blob/main/docs/development-log.md)


<a id="findability-test"></a>
### Findability as a test

Summary
: Generate an outline from every module's first sentence, then ask it real questions in a test ("where is it said which kind of disk we work with?") and fail if the answer is not near the top. A cold read, turned into something that runs on every change. If a description is vague, or a thing is in the wrong place, it shows here first.

Tags
: measure, guard

Relations
: → extends: [The stranger test](concepts.md#stranger-test) — the stranger test, run on every change

Sources
: [snapall: a Rust command line and terminal UI over snapper, the worked example of everything in this playbook](https://github.com/grenudi/snapall)


<a id="guards-are-tests"></a>
### Guards are tests that read the source

Summary
: Architecture rules are ordinary tests that read the source tree (or its parsed form) and fail naming the file and line. A rule that lives only in a document is a wish; a rule that fails the build is a property of the project.

Tags
: guard

Relations
: ← enforced-by: [A fact, a word or a rule lives in one place](concepts.md#one-fact-one-place) — a copy of a sentence or a rule is a failing test
: ← part-of: [Debts are data and only shrink](concepts.md#ratchet)
: ← needs: [Prove every guard bites](concepts.md#prove-the-guard-bites)
: ← part-of: [Pin the real output](concepts.md#golden-output)
: ← enforced-by: [Retire a word with a guard](concepts.md#retire-words)
: ← enforced-by: [Documents are checked against the code](concepts.md#docs-tell-the-truth)

Sources
: [snapall: a Rust command line and terminal UI over snapper, the worked example of everything in this playbook](https://github.com/grenudi/snapall)


<a id="ratchet"></a>
### Debts are data and only shrink

Summary
: A rule that cannot be met today is recorded as a number per file in a data file. The test fails if any number grows, and insists the file record any decrease. Progress cannot silently slip back, and what remains is a list anyone can read.

Tags
: guard, measure

Relations
: → part-of: [Guards are tests that read the source](concepts.md#guards-are-tests)

Sources
: [snapall: a Rust command line and terminal UI over snapper, the worked example of everything in this playbook](https://github.com/grenudi/snapall)


<a id="prove-the-guard-bites"></a>
### Prove every guard bites

Summary
: A guard that has only ever passed is unproven. Break the thing it guards on purpose, in a clean file, confirm it fails with a useful message, then restore the file *exactly* (and compare). Two checks can pass together for the wrong reason, for example a link and its target both wrong in the same way, so test the rule against the outside truth too.

Tags
: guard, discipline

Relations
: → needs: [Guards are tests that read the source](concepts.md#guards-are-tests)
: ← extends: [Check the property, not the symptom](concepts.md#check-the-property)

Sources
: [snapall development log: what was done, why, the evidence and the mistakes, newest first](https://github.com/grenudi/snapall/blob/main/docs/development-log.md)


<a id="check-the-property"></a>
### Check the property, not the symptom

Summary
: A compile, a green build or a passing test is not the check that a change did what you meant. Check the property itself: that no string literal changed under a rename, that the output is byte-identical, that the real program says what you think it says. Almost every surprise in this project was a symptom taken for the property.

Tags
: discipline

Relations
: → extends: [Prove every guard bites](concepts.md#prove-the-guard-bites)
: ← extends: [Tools that rewrite code verify themselves](concepts.md#tools-verify-themselves)
: ← needs: [Remove a race by construction](concepts.md#race-by-construction)
: ← needs: [Search by shape, and read all of the results](concepts.md#search-by-shape)
: ← extends: [Generalise a tool with a parity test](concepts.md#generalise-with-a-parity-test) — the property is: it still does what the original did

Sources
: [snapall development log: what was done, why, the evidence and the mistakes, newest first](https://github.com/grenudi/snapall/blob/main/docs/development-log.md)


<a id="measure-before-and-after"></a>
### Measure before you claim

Summary
: Say how long, how many, how big, before and after, with the samples, and say when the samples overlap. A claim chosen from the best runs is not a measurement. When you find you overclaimed, retract it in writing, where the claim was made.

Tags
: discipline, measure

Relations
: ← needs: [Measure the CI before optimising it](concepts.md#measure-the-ci-first)

Sources
: [snapall development log: what was done, why, the evidence and the mistakes, newest first](https://github.com/grenudi/snapall/blob/main/docs/development-log.md)


<a id="seeded-cold-reads"></a>
### Seeded cold reads

Summary
: Pick modules at random with a seed (so the read is reproducible), read them as a stranger, and write down where you stumbled. It finds what no guard measures: a rule copied by hand, a stale word, a distinction the code makes and never names. It stops paying when a seed returns modules you have already read; that is the signal to read differently.

Tags
: measure, reading

Relations
: → extends: [The stranger test](concepts.md#stranger-test)
: ← extends: [Use the program as a newcomer would](concepts.md#use-it-as-a-newcomer) — when reading code stops finding things

Sources
: [snapall: a Rust command line and terminal UI over snapper, the worked example of everything in this playbook](https://github.com/grenudi/snapall)


<a id="use-it-as-a-newcomer"></a>
### Use the program as a newcomer would

Summary
: Run the real program on a real disk, from first use to going back, and read every word it says; drive a terminal UI through a pseudo-terminal and print its screens. Reading code finds what is wrong with code; only using the program finds what is wrong with what it *says*.

Tags
: reading, clarity

Relations
: → extends: [Seeded cold reads](concepts.md#seeded-cold-reads) — when reading code stops finding things
: ← extends: [Look at what people will see](concepts.md#look-at-what-people-see) — for what is seen rather than read

Sources
: [snapall: a Rust command line and terminal UI over snapper, the worked example of everything in this playbook](https://github.com/grenudi/snapall)


<a id="golden-output"></a>
### Pin the real output

Summary
: Record the exact text of the program's commands on a real fixture, and fail CI when it differs. A change to wording then shows as the few lines that moved, reviewed as such. Re-record only after reading the diff: a recording of empty output looks as clean as a good one until you read it.

Tags
: guard, output

Relations
: → part-of: [Guards are tests that read the source](concepts.md#guards-are-tests)

Sources
: [snapall development log: what was done, why, the evidence and the mistakes, newest first](https://github.com/grenudi/snapall/blob/main/docs/development-log.md)


<a id="tools-verify-themselves"></a>
### Tools that rewrite code verify themselves

Summary
: A splitter, a renamer or a formatter that edits many files checks its own work: every comment survives, no string literal changed, nothing is written unless everything matches. A regex rename once changed a JSON key and a fake tool's output; a lexer-based one that verifies the strings changed none.

Tags
: automation, discipline

Relations
: → extends: [Check the property, not the symptom](concepts.md#check-the-property)
: ← needs: [Retire a word with a guard](concepts.md#retire-words)
: ← needs: [Generalise a tool with a parity test](concepts.md#generalise-with-a-parity-test)

Sources
: [snapall: a Rust command line and terminal UI over snapper, the worked example of everything in this playbook](https://github.com/grenudi/snapall)


<a id="automate-repeated-hand-work"></a>
### Automate what you do twice by hand

Summary
: The second time a manual step is repeated, build the tool, document it in the repository's agent notes and log, and use cheap compute (CI) where it can. The ship script, the gate, the splitter, the scans and the timing report each began as a step done by hand twice.

Tags
: automation

Relations
: → needs: [State and plans live in the repository](concepts.md#state-in-the-repo) — the tool is documented in the repository, or the next agent rebuilds it
: ← part-of: [A stateless, resumable shipper](concepts.md#resumable-shipper)
: ← part-of: [A fast local gate; CI for the rest](concepts.md#fast-gate)

Sources
: [snapall development log: what was done, why, the evidence and the mistakes, newest first](https://github.com/grenudi/snapall/blob/main/docs/development-log.md)


<a id="state-in-the-repo"></a>
### State and plans live in the repository

Summary
: An agent's memory is not the project's memory. The plan (backlog), the decisions (log), the rules (agent notes) and the documentation of the tools are files in the repository, so no session starts over and any agent can continue where another stopped.

Tags
: process

Relations
: ← needs: [Automate what you do twice by hand](concepts.md#automate-repeated-hand-work) — the tool is documented in the repository, or the next agent rebuilds it
: ← needs: [One branch, one merged pull request per iteration](concepts.md#branch-per-iteration)

Sources
: [tad-engine: the text-as-data engine this repository is built on](https://github.com/creation-guidelines/tad-engine), [git-subrepo: vendor another repository as a folder, and pull updates into it](https://github.com/ingydotnet/git-subrepo)


<a id="branch-per-iteration"></a>
### One branch, one merged pull request per iteration

Summary
: Each iteration is a branch from the current main, a pull request whose body says what and why and shows the evidence, and a squash merge with a conventional title. History reads as the story of the work, and nothing depends on a conversation.

Tags
: process

Relations
: → needs: [State and plans live in the repository](concepts.md#state-in-the-repo)
: ← needs: [A stateless, resumable shipper](concepts.md#resumable-shipper)

Sources
: [Conventional Commits 1.0.0](https://www.conventionalcommits.org/)


<a id="resumable-shipper"></a>
### A stateless, resumable shipper

Summary
: One script pushes, opens the pull request, waits for checks, merges and verifies. It keeps no state of its own, reading GitHub every time, and it stops itself before the tool's time limit with a code that means *run me again*. Any session can continue what another began.

Tags
: automation, process

Relations
: → part-of: [Automate what you do twice by hand](concepts.md#automate-repeated-hand-work)
: → needs: [One branch, one merged pull request per iteration](concepts.md#branch-per-iteration)
: ← part-of: [Judge CI by the newest run of each check](concepts.md#newest-run-counts)

Sources
: [snapall: a Rust command line and terminal UI over snapper, the worked example of everything in this playbook](https://github.com/grenudi/snapall)


<a id="fast-gate"></a>
### A fast local gate; CI for the rest

Summary
: One command runs what must pass before shipping (format, lint, docs, links, licences, tests), writes each step's log to a file and prints one line per step. CI runs the heavy matrix. The gate is for reproducing a failure and for catching mistakes early, not a substitute for the pull request.

Tags
: automation, process

Relations
: → part-of: [Automate what you do twice by hand](concepts.md#automate-repeated-hand-work)

Sources
: [snapall: a Rust command line and terminal UI over snapper, the worked example of everything in this playbook](https://github.com/grenudi/snapall)


<a id="newest-run-counts"></a>
### Judge CI by the newest run of each check

Summary
: Reruns and flakes leave old failures in the history. Judge a commit by the newest run of each check name, count skipped as passing, and rerun a job the runner itself failed to start. A release is the commit titled as one, not the merge before it.

Tags
: process, ci

Relations
: → part-of: [A stateless, resumable shipper](concepts.md#resumable-shipper)

Sources
: [snapall development log: what was done, why, the evidence and the mistakes, newest first](https://github.com/grenudi/snapall/blob/main/docs/development-log.md)


<a id="measure-the-ci-first"></a>
### Measure the CI before optimising it

Summary
: Collect wall time, job-minutes and the slowest jobs and steps over several runs, then change the critical path. The biggest win here was one step, a security audit that compiled its own tool for three minutes. Reject, with reasons, what the measurement does not support.

Tags
: ci, measure

Relations
: → needs: [Measure before you claim](concepts.md#measure-before-and-after)
: ← extends: [The levers that paid](concepts.md#ci-small-levers)
: ← extends: [Release in batches, not on every merge](concepts.md#batch-releases)

Sources
: [snapall development log: what was done, why, the evidence and the mistakes, newest first](https://github.com/grenudi/snapall/blob/main/docs/development-log.md)


<a id="ci-small-levers"></a>
### The levers that paid

Summary
: A prebuilt tool instead of compiling it; a timeout on every job; the cache saved only from main; narrower triggers so a documents-only change skips the heavy jobs; no incremental builds or full debug info in CI; retries on the network. A policy swap (here, the audit's rules) was proven locally against a known-bad case before it replaced the old one.

Tags
: ci

Relations
: → extends: [Measure the CI before optimising it](concepts.md#measure-the-ci-first)

Sources
: [snapall: a Rust command line and terminal UI over snapper, the worked example of everything in this playbook](https://github.com/grenudi/snapall), [cargo-deny: lint the dependency graph (advisories, licences, bans)](https://github.com/EmbarkStudios/cargo-deny), [Swatinem/rust-cache: cache Rust build artefacts in GitHub Actions](https://github.com/Swatinem/rust-cache)


<a id="batch-releases"></a>
### Release in batches, not on every merge

Summary
: A release per merge costs minutes of waiting and gives users a new version every few minutes, while proving little that CI does not. Release when about ten changes wait, or the oldest has waited a week, or a change touches how releases are *published* (the one thing only a release proves), or on request. Make the policy a small tested function.

Tags
: ci, process

Relations
: → extends: [Measure the CI before optimising it](concepts.md#measure-the-ci-first)

Sources
: [snapall: a Rust command line and terminal UI over snapper, the worked example of everything in this playbook](https://github.com/grenudi/snapall), [release-plz: release pull requests and changelogs from conventional commits](https://release-plz.dev/)


<a id="race-by-construction"></a>
### Remove a race by construction

Summary
: A rare failure is not disproved by many clean runs on a fast machine. Find the shared resource, put every use behind one lock, and show with a stress test that the original fails and the fixed version does not.

Tags
: discipline, ci

Relations
: → needs: [Check the property, not the symptom](concepts.md#check-the-property)

Sources
: [snapall development log: what was done, why, the evidence and the mistakes, newest first](https://github.com/grenudi/snapall/blob/main/docs/development-log.md)


<a id="retire-words"></a>
### Retire a word with a guard

Summary
: When a word is wrong (here, *config* for an area), rename its uses with a lexer-based tool that follows string interpolation and verifies no literal changed, then add a guard that the word is not an identifier outside the adapter that owns it.

Tags
: clarity, guard

Relations
: → needs: [Tools that rewrite code verify themselves](concepts.md#tools-verify-themselves)
: → enforced-by: [Guards are tests that read the source](concepts.md#guards-are-tests)
: ← extends: [Published identities are not renamed for a word](concepts.md#published-names-stay) — the exception that is written down

Sources
: [snapall development log: what was done, why, the evidence and the mistakes, newest first](https://github.com/grenudi/snapall/blob/main/docs/development-log.md)


<a id="published-names-stay"></a>
### Published identities are not renamed for a word

Summary
: A key in a JSON output, a contract's identity, a stored word in a journal: other programs and older files read them. Give people a plain word beside the stored one, test both, and leave the stored one alone, with the reason written down.

Tags
: clarity, discipline

Relations
: → extends: [Retire a word with a guard](concepts.md#retire-words) — the exception that is written down

Sources
: [snapall development log: what was done, why, the evidence and the mistakes, newest first](https://github.com/grenudi/snapall/blob/main/docs/development-log.md)


<a id="docs-tell-the-truth"></a>
### Documents are checked against the code

Summary
: A document that names a path is checked to name a real one; a code example in a document is compared with the source; a page about how close the code is to the ideal says where it is not close. A guess written as fact is corrected in writing when it turns out wrong, and so is an invented date.

Tags
: guard, clarity

Relations
: → enforced-by: [Guards are tests that read the source](concepts.md#guards-are-tests)

Sources
: [reStructuredText: the markup specification and docutils](https://docutils.sourceforge.io/rst.html)


<a id="plain-reports"></a>
### Report in plain words, at the big picture

Summary
: Say what changed, how much closer it is to the ideal, what went wrong, and what is next, in language a person who does not read the code can follow. Technical detail belongs in the log and the pull request. Own mistakes briefly and say what they taught.

Tags
: process, communication

Relations
: ← needs: [Decide, following the canon and the project's interest](concepts.md#decide-yourself)

Sources
: [snapall development log: what was done, why, the evidence and the mistakes, newest first](https://github.com/grenudi/snapall/blob/main/docs/development-log.md)


<a id="decide-yourself"></a>
### Decide, following the canon and the project's interest

Summary
: An agent given a principle decides, and says what it decided and why, instead of handing the choice back. It asks only when the answer needs something it cannot know, and it checks between iterations that each action still serves the purpose and is not busy work.

Tags
: process, communication

Relations
: → needs: [Report in plain words, at the big picture](concepts.md#plain-reports)

Sources
: [snapall development log: what was done, why, the evidence and the mistakes, newest first](https://github.com/grenudi/snapall/blob/main/docs/development-log.md)


<a id="search-by-shape"></a>
### Search by shape, and read all of the results

Summary
: To find a smell, search by its *shape* (every bare bool in a pair, every `if n == 1`), not by the instance you noticed. Read the whole result: a search cut off after ten lines once hid the one script that pinned a change, and CI found it.

Tags
: reading, discipline

Relations
: → needs: [Check the property, not the symptom](concepts.md#check-the-property)

Sources
: [snapall development log: what was done, why, the evidence and the mistakes, newest first](https://github.com/grenudi/snapall/blob/main/docs/development-log.md)


<a id="say-what-to-do-next"></a>
### Say what to do next, once

Summary
: Every situation where nothing is there, or something failed, says what to do about it, in the layer that owns the words, so every surface (command line, window) is equally helpful and none repeats it differently.

Tags
: clarity, output

Relations
: → needs: [A fact, a word or a rule lives in one place](concepts.md#one-fact-one-place)

Sources
: [snapall development log: what was done, why, the evidence and the mistakes, newest first](https://github.com/grenudi/snapall/blob/main/docs/development-log.md)


<a id="generalise-with-a-parity-test"></a>
### Generalise a tool with a parity test

Summary
: When a script built for one project is made general, run the general one and the original on the original's own project and compare the results. If they differ, form a hypothesis and test it with a controlled experiment (give the new one the old one's exact rule and see whether the results then match) until every difference is explained and deliberate. A generalisation that is 'about the same' has changed something nobody chose.

Tags
: discipline, automation

Relations
: → extends: [Check the property, not the symptom](concepts.md#check-the-property) — the property is: it still does what the original did
: → needs: [Tools that rewrite code verify themselves](concepts.md#tools-verify-themselves)

Sources
: [snapall: a Rust command line and terminal UI over snapper, the worked example of everything in this playbook](https://github.com/grenudi/snapall)


<a id="look-at-what-people-see"></a>
### Look at what people will see

Summary
: A check that a page answers, or that every link on it resolves, cannot see that it looks wrong. Look at it the way a reader will: a screenshot of the real page in a real browser, of the live site and not only of a local build. Three defects of this playbook's own site (literals not styled as code, a table of contents drawn like the navigation bar, headings drawn as links) were visible only that way.

Tags
: reading, output

Relations
: → extends: [Use the program as a newcomer would](concepts.md#use-it-as-a-newcomer) — for what is seen rather than read

Sources
: [This playbook's lessons chapter: each mistake, and the rule it became](https://github.com/creation-guidelines/ideal-project-playbook/blob/main/playbook/08-lessons.rst)


<a id="look-around-first"></a>
### Look around first

Summary
: Before acting, take a clear look at the situation: what is, what we are dealing with, why it is so, and what others already learned. Keep what was found as research - the question, the findings, their sources - so the decisions that rest on it can cite it, and anyone can follow a step down to what it stands on.

Tags
: practice, research

Sources
: [The OODA loop: observe, orient, decide, act](https://en.wikipedia.org/wiki/OODA_loop), [The Thing: Why I Am a Catholic (the fence)](https://en.wikipedia.org/wiki/G._K._Chesterton#Chesterton's_fence), [The Toyota Way (go and see)](https://en.wikipedia.org/wiki/Genchi_Genbutsu)


<a id="words-are-decisions"></a>
### Words are decisions

Summary
: Choose each word as a decision: look at what others call the thing and what the reader already knows, prefer the plain word with one meaning, and keep the choice with the words rejected and the reasons. One language, used the same way in talk, in code and in documents.

Tags
: practice, language

Sources
: [Federal Plain Language Guidelines](https://www.plainlanguage.gov/guidelines/), [Politics and the English Language](https://www.orwellfoundation.com/the-orwell-foundation/orwell/essays-and-other-works/politics-and-the-english-language/), [Domain-Driven Design (the ubiquitous language)](https://www.domainlanguage.com/ddd/)
