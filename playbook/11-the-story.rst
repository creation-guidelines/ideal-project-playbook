The story: how it was actually done
===================================

The practices read as a plan. They were not one. They came, in this order, out of things that went wrong or were done twice. The dates are from git: the whole of it took about eight days (2026-10-26 to
2026-11-03), a person and an agent working together, most of it with the agent chaining iterations on its own.

1. The idea, and a first measure (about 0.25 to 0.27)
-----------------------------------------------------

The project already worked. The aim was clarity. The core was reorganised into folders named for what the program is for, one command was rewritten as a story of named steps and kept as the worked example, and the
idea was written down in one page for the canon. Then the first honest question: *how would we know we were getting closer?* A script compared the code with earlier releases (``structure-metrics``) and the first guards
were written as tests (a file is short enough to read whole; no printing outside the output module). The shipper and the fast gate were built when the same ten steps had been typed for the second time.

2. Reading, and turning each find into a guard
----------------------------------------------

A *seeded cold read* of random modules found real things every time: stale words, a rule copied in five commands, a distinction made and never named. Each became a fix **and a test**, so it could not come back.
Rules the code could not yet satisfy went into the *ratchet*, as numbers that may only shrink, and the debt, a list, was paid down to a single deliberate entry within days. The nouns that appeared (``Counting``,
``Found``, ``Agreed``, ``Pick``, ``counted``) were each a distinction the code had been making all along.

3. The incidents that made the tools verify themselves
-------------------------------------------------------

A regex rename of a wrong word changed a JSON key and a fake tool's output without any test noticing. The renamer became a lexer-based tool that checks no string literal changed. A splitter lost a comment once; it now
refuses to write unless every comment survives. A race that 740 clean runs had "disproved" failed in CI; it was removed by construction and stress-tested. Each of these is a rule in ``08-lessons``.

4. The cold read becomes a test
-------------------------------

The outline and the findability questions turned the best finder of problems into a check that runs on every change. 52 questions; all answers within the first three.

5. The CI, measured then optimised
----------------------------------

Asked to "research the best CI optimisations and apply them", the first step was to measure: eight runs, median 193 seconds and 20 job-minutes. One step was 181 seconds of compiling a tool. The levers that paid,
and the ones rejected with reasons, are in ``06-ci-and-releases``. One claim was retracted in the log when later data showed it had been read off the best runs.

6. Scans, and a report that was too technical
---------------------------------------------

A scan for repeated code found, in one pass, what reading finds one module at a time. And the person said the reports were cumbersome and technical: the standing instruction became *short, plain, big-picture,
how much closer to the ideal*. The reports changed; the technical detail moved to the log and the pull request where it belongs.

7. When reading stopped paying
------------------------------

A seed returned modules already read. The method changed: the program was *used as a newcomer would*, on a real fixture and through a pseudo-terminal, and every word was read. That found what no code reading had
(zeros in a preview, a missing "what is this restore point called?", a leaked retired word), and the same kind of defect in the singular and the zero. The man page then showed that a hint ignored its own switch.

8. The release policy
---------------------

The person asked whether a release per merge made sense. It did not: it cost eight minutes each and proved little that CI did not. Releases were batched by a tested policy. Each iteration then took two tool calls
instead of six.

9. The record was checked, and was wrong
----------------------------------------

Preparing this playbook from the development log, 51 of its 52 dates turned out to be counted forward a day per entry. They were corrected from git, and the rule "dates come from the clock" was added. It is the clearest
single example of the last rule in ``kit/AGENT-INSTRUCTIONS.rst``: a record that is not checked is a record that cannot be trusted.

10. The playbook
----------------

The same machinery produced this repository: the text-as-data engine learned to write reStructuredText (with its first tests), the template was updated, and this repository was generated from it, as data and as prose.

What did not happen
-------------------

None of this has been tried on a second project, and none of it has run on the person's own machine. Those are the honest next tests (see the backlog in ``docs/backlog.rst``).
