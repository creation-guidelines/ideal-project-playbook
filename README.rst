ideal-project-playbook
======================

How to run any software project to an ideal of **clarity and elegance** with an agent: the idea, the loop, the guards, the automation, and the mistakes that
taught each rule. It was learned on one real project and is written so that you can hand it to an agent and start another.

Read it as a site: https://creation-guidelines.github.io/ideal-project-playbook/ (built from the same files by ``tools/build_site.py``).

Use it in one step
------------------

Give an agent ``kit/AGENT-INSTRUCTIONS.rst`` and one sentence:

    *Manage the project in this repository following AGENT-INSTRUCTIONS.rst. Read all of it first. Decide for yourself, report as it says, and keep going without
    waiting for me.*

That file is complete on its own: the purpose, the standing orders, the day-one setup, the iteration loop, what to build and in what order, the guards to write,
the ways of reading that find what tests cannot, the CI and release rules, the honesty rules, and the shape of a report.

The one idea
------------

**Every layer is the top of the layers beneath it.** Read from the top, each part says what it is *for* in the words a person uses; each step down says *how*, using only
the words of the layer beneath. Every part has an upward face (its purpose) and a downward face (a body in the words below), and a part that cannot be described that way
is doing two jobs. The measure is the *stranger test*: someone who has never seen the code reads a part's first line and can say what it is for, and is right.

What is here
------------

``kit/AGENT-INSTRUCTIONS.rst``
    The document to hand to an agent.
``playbook/``
    The reasons and the stories, in eleven chapters (start at `playbook/index.rst <playbook/index.rst>`__).
``kit/``
    The tested tools, templates and CI configuration (map: ``kit/README.rst``): the guards (ratchet, outline, findability ranking, a catalogue of architecture rules), the shipper and its
    release policy, the gate, golden output, a screen driver for terminal programs, structure metrics, the scans, the starting files for a project, CI and release configuration, and the
    two tools that rewrite code (a splitter and a lexer-based renamer).
``docs/``
    The same knowledge as **data**, rendered: 33 practices and how they relate (``docs/concepts.rst``), the decisions with what was considered and rejected (``docs/session_log.rst``),
    sources, and the backlog.

The worked example
------------------

Everything here was learned on `snapall <https://github.com/grenudi/snapall>`__, a Rust command line and terminal UI over snapper. Its `idea page <https://github.com/grenudi/snapall/blob/main/docs/the-idea.md>`__, `development log <https://github.com/grenudi/snapall/blob/main/docs/development-log.md>`__,
`agent notes <https://github.com/grenudi/snapall/blob/main/AGENTS.md>`__ and `dev/ <https://github.com/grenudi/snapall/tree/main/dev>`__ are the idea, the log, the rules and the tools in use;
its `architecture <https://github.com/grenudi/snapall/blob/main/crates/snapall/tests/architecture.rs>`__ and `findability <https://github.com/grenudi/snapall/blob/main/crates/snapall/tests/findability.rs>`__ tests are the guards.

How this repository is built
----------------------------

It is generated from `text-as-data-template <https://github.com/creation-guidelines/text-as-data-template>`__: the knowledge is kept as plain versioned **data** (``data/``, JSON lines declared by ``tables.toml``), the engine (`tad <https://github.com/creation-guidelines/tad-engine>`__, a released Rust tool) guards and canonicalises it, and the pages in ``docs/``
are **rendered** from it. This repository renders **reStructuredText** (``DOCS_FORMAT=rst``), a format the engine learned for it; the prose in ``playbook/`` and ``kit/`` is hand-written ``.rst``.
See ``AGENTS.rst`` for how to work in it.

Status
------

Early. The honest next test is a **second project in another language** (see ``docs/backlog.rst``): nothing here has been tried beyond the project it came from, and it has not run on the author's own
machine yet. The kit's guards are tested on small fixtures. No licence has been chosen for the text; the scripts in ``kit/scripts/`` carry the SPDX headers they had in ``snapall`` (GPL-3.0-or-later).
