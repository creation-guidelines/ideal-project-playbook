AGENTS - how to work in this repository
=======================================

This repository holds a playbook for running projects to an ideal of clarity. It has two kinds of content, and the rules differ.

**Prose** (hand-written ``.rst``): ``README.rst``, ``AGENTS.rst``, ``CONTRIBUTING.rst``, ``playbook/``, ``kit/*.rst``. Edit these directly. They must stay valid: ``make rst`` (docutils, every warning a failure).

**Data** (generated pages): the practices, decisions, sources and backlog live as data in ``data/``. The pages in ``docs/`` are *rendered* from it and must never be edited by hand.

Follow the playbook in this repository's own work: ``kit/AGENT-INSTRUCTIONS.rst``. In particular: decide for yourself, one branch and one merged pull request per iteration, log what you did and why, dates from ``date``, and finish every change with ``make verify``.

Setup (once per session)
------------------------

::

    make setup    # installs tad (the data engine, a released Rust binary) and the tools' Python packages
    make test     # tests for kit/guards and kit/scripts
    make verify   # data valid and canonical, pages fresh: what CI runs
    make rst      # every reStructuredText file is valid

Layout
------

- ``kit/AGENT-INSTRUCTIONS.rst``: the document handed to an agent (prose).
- ``playbook/*.rst``: the chapters (prose).
- ``kit/guards/``, ``kit/scripts/``: reusable code, with tests (``make test``).
- ``tables.toml``: every table declared as data - its fields, types, allowed values and patterns - and the rules across tables. The authority on what the data may hold.
- ``data/<table>.json``: the data, one JSON object per line. Change it with ``tad``, never by hand.
- ``docs/*.rst``: rendered pages. ``make render`` only.

The data engine is `tad <https://github.com/creation-guidelines/tad-engine>`__, installed from its pinned release by ``bin/install-tad.sh``.

Rules for the data
------------------

1. **Never hand-edit** ``data/*.json`` **or anything in** ``docs/``. Change a row with ``tad set``; it checks the whole repository and keeps nothing that breaks a rule. Then ``make render``.
2. **Always finish with** ``make verify``: tad must write the final bytes (``tad canon``), or CI fails on a non-canonical diff.
3. **Every id in every table shares one namespace**, and both ends of every relation must exist: the rules ``unique_ids`` and ``references`` in ``tables.toml``.
4. **A factual claim needs a source.** Every practice cites at least one, through ``concept_sources`` (the rule ``appears_in``). A practice learned on a project cites where it was learned; one taken from a reference cites the reference.
5. A value may use the Markdown inline subset (code, links, bold, emphasis); tad converts it for reStructuredText.
6. **Add a practice** as a ``concepts`` row with the *what* and the *why*, relate it to what it needs or extends in ``relations``, cite it in ``concept_sources``, and record any decision about it in ``session_log`` with what was considered and rejected. Record each working session in ``session_log`` the same day, with the date from ``date``.

Recipes
-------

Add or change content::

    tad set concepts --key an-id --set "name=Name" --set "summary=What it is, and why." --set tags=tag
    tad set concept_sources --key an-id --key snapall-log
    tad set concepts --key an-id --set "summary=..."
    make render && make verify

A new field: declare it in ``tables.toml`` (a ``[[tables.<table>.fields]]`` entry with its ``name`` and ``type``, and ``required``, ``enum`` or ``pattern`` if it has them), then ``make canon``: every line gains the field, empty. A required field is then given a value on every row with ``tad set`` before ``make verify`` passes.

Rename a field: ``mlr -I --ijsonl --ojsonl rename old,new data/<table>.json``, make the same change in ``tables.toml``, then ``make canon`` (forgetting the declaration is caught by ``make check``).

Build and look at the site: ``make site`` writes ``_site/``. Look at the pages in a browser before relying on them: a structural check cannot see that a page looks wrong.

Why it is built this way
------------------------

- The data is plain text in git: one JSON object per line, so a change to one row is a one-line diff, readable without any tool.
- ``tables.toml`` declares the tables as data (after Frictionless Data's Table Schema): a person reads it, and tad checks every row and every rule across tables against it.
- The renderer is schema-agnostic: it detects a relations table and a sources table by their *shape*, not their name, so a new table needs no configuration.
- GitHub Pages does not render reStructuredText, so ``tools/build_site.py`` does, with docutils alone, and fails on any broken link or anchor.
- tad replaced a vendored Python engine (DuckDB) on 2026-11-11, after giving the same verdicts, the same canonical bytes and the same documents on this repository and three others.

Output format
-------------

This repository renders reStructuredText: ``export DOCS_FORMAT ?= rst`` in the ``Makefile``. ``DOCS_FORMAT=md,rst make render`` writes both if you need to compare.

Commits
-------

Conventional Commits, linted on the pull request; squash merges. See ``CONTRIBUTING.rst``.
