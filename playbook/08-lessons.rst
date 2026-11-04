Lessons: the mistakes, and the rule each became
================================================

None of these is a failure of the method; each is a place where the method needed a rule it did not yet have. They are listed because an agent will meet
the same ones. The format is the mistake, then what it taught.

A regex rename that lied
    Two regular-expression renames of a retired word changed a JSON key and a fake tool's raw-string output while every test stayed green. *Taught:* check the property
    (no string literal changed), not the symptom (it compiles); build the renamer on a lexer and make it verify and revert.

A race measured away
    740 clean local runs "showed" a spawn race was gone; CI then failed with *text file busy*. *Taught:* many clean runs on a fast machine are weak evidence against a rare race.
    Remove it by construction and stress-test the original and the fix.

A claim chosen from the best runs
    A CI speed-up was reported from the best of a few runs, and later retracted when the ranges overlapped. *Taught:* measure with samples, say when they overlap, retract in writing
    where the claim was made.

A search cut off after ten lines
    The real-terminal script that pinned a changed wording never appeared in a truncated search; CI found it. *Taught:* read all of any search result, or narrow the pattern until the
    results are few.

A guess written as fact
    The idea page said the adapters were the part least like the ideal. Reading each by its first line showed the opposite. *Taught:* a guess is written as a guess; and a document that
    judges the code is checked against the code.

Dates that were counted
    Fifty-one of fifty-two headings in a development log carried dates counted forward a day per entry, found only because a playbook was being written from it. Git said the work took eight
    days. *Taught:* take the date from ``date`` or git; add the rule to the agent notes; a record with invented dates cannot be trusted for anything else in it.

A recording of nothing
    Golden output re-recorded from a second working copy, where the program was not at the expected path, showed 1,096 deleted lines across all 20 files. *Taught:* read the diff of a
    recording before committing it.

A new tip that ignored its own switch
    A hint added beside an existing option ignored the option that silences hints. *Taught:* wire a new thing to the switch it lives beside, and read the switch's documentation.

An idiom list that was incomplete
    The plural guard looked for ``if n == 1`` in a list of known wordings and missed ``snapshot(s)``. *Taught:* make the guard recognise the *shape* of the defect, not the instances
    seen so far; and for a pattern that appears harmlessly in code (``(s)``), count it only inside strings.

Editing by exact text
    A script edited an export list by its exact text after the formatter had rewrapped it: the first edit applied, the rest did not, and the build still passed (with only an unused-constant warning).
    Removing "the last closing brace" of a file assumed a wrapper module that was not there. *Taught:* a script that edits several files must apply all or nothing; look at the shape of
    a file before editing by it; "it compiled" is not evidence that the edit did what you meant; edit an identifier, not a line's text.

A fixture that was gone
    A fixture torn down by an earlier test run made a later check meaningless ("snapper failed: reading failed"). *Taught:* bring the fixture up at the start of every check that needs it.

A slow step and a long wait in one call
    The gate plus a 235-second wait exceeded the tool's 300-second limit. *Taught:* split work across calls; make every long process resumable; nothing started in a call outlives it.

A zero that was not "no"
    Making the counting helper say *no snapshots* for zero turned *0 seconds* into *no seconds*; a failing test said so. *Taught:* a measure keeps its zero; say so explicitly at that site.

An ambiguous label
    An Activity entry from the command line said *(command)*: the journal's stored word doing double duty as the displayed one. *Taught:* a stored word and a word for people are two words; the core owns both.

A branch that lacked recent merges
    A failed shell line skipped its own ``git pull``; the branch conflicted with main, got no CI, and the shipper waited on silence. *Taught:* branch from ``origin/main`` explicitly; make the shipper
    name a conflicting pull request.

A note written before its anchor existed
    A log note was inserted after a heading that a stale local copy of the file did not yet have, so it was silently not written (twice). *Taught:* rebase onto fresh main before editing a file by
    an anchor; and check that the edit landed.

Tests that pinned what they should not have
    Eight things pinned an old wording after a one-word change (four tests, a real-terminal script, two golden files). *Taught:* that is the guards doing their job; the work is to find every pin,
    update it, and look at the golden diff.

A defect found by reading the documentation, not the code
    Both the ignored switch and a leaked word were found in the manual and in a header, not in a function. *Taught:* read what the program says, not only what it is.

A generalised script that was not identical
    The repeated-code scan, rewritten to be language-neutral, reported 12 repeated runs where the original reported 11. *Taught:* compare the general tool with the original on the original's own project; when they differ, form a hypothesis and
    test it with a controlled experiment. Giving the new scanner the original's exact rule made the results match exactly (11 and 223), which proved the one remaining difference was deliberate (it also ignores closers such as ``});``).

A hidden-directory check that hid everything
    The outline extractor skipped directories whose path had a component starting with a dot, and a root given as ``.`` or ``..`` has such components, so it listed zero modules. *Taught:* run a new tool on the repository that contains it,
    immediately; and every bug found that way gets a regression test, here one for a root of ``.`` and of ``..``.

A first sentence that failed its own test
    The repository's own findability questions did not lead to the gate script ("how do I run every check before pushing?"), because its first sentence said it ran what "has to pass before a change is shipped". *Taught:* that is the test
    working: the description, not the test, was wrong, and it now says *every check ... before a change is pushed*.

Documents that named another project's files
    A path check on this repository's own prose found twelve names that were not files here: a bare extension, shorthand like *findability.py* where ``kit/guards/findability.py`` was meant, and snapall's own files written as if they were
    local. *Taught:* a path in a document is either a file that exists in this repository, or a link into the repository it belongs to.

A refused recording that still changed things
    The golden-output script refused to record a program that printed nothing, but had already written the empty recordings into the golden directory, where they could be committed. *Taught:* a refusal must change nothing; record into a
    temporary directory and move it into place only after validation, and test that an existing recording is byte-for-byte untouched by a refused one.

A shell feature in the wrong shell
    A loop using ``<<<`` failed because the tool's shell is ``sh``. *Taught:* put anything with a shell feature in a script run by ``bash``, and keep one-line commands portable.

A claim about a platform that I had not checked
    Switching the repository to reStructuredText, I deleted the template's Jekyll files and wrote that GitHub renders ``.rst`` itself. It does, in the file browser, but GitHub Pages does not, so there was no site at
    all, and the person had to tell me. *Taught:* before removing something that did a job, check what replaces it, by trying it; a claim about what a platform does is a guess until it has been seen to work. The fix was a
    small builder (docutils, the reference implementation) that fails the build on any broken link or anchor.

A tool that assumed its own repository
    The first test of the site builder, run against a minimal repository, crashed because it assumed the agent instructions existed. *Taught:* test a tool on a repository that is not yours as soon as it exists; its first assumption is its first bug.

