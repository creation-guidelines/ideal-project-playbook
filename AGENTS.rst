AGENTS - how to work in this repository
=======================================

This repository holds a playbook for running projects to an ideal of clarity. It has two kinds of content, and the rules differ.

**Prose** (hand-written ``.rst``): ``README.rst``, ``AGENTS.rst``, ``CONTRIBUTING.rst``, ``playbook/``, ``kit/*.rst``. Edit these directly. They must stay valid: ``make rst`` (docutils, every warning a failure).

**Data** (generated pages): the practices, decisions, sources and backlog live as data in ``data/``. The pages in ``docs/`` are *rendered* from it and must never be edited by hand.

Follow the playbook in this repository's own work: ``kit/AGENT-INSTRUCTIONS.rst``. In particular: decide for yourself, one branch and one merged pull request per iteration, log what you did and why, dates from ``date``, report plainly.

Setup (once per session)
------------------------

::

    make setup    # pins DuckDB (pip) and Miller (mlr) to the versions .tad/bootstrap.sh installs
    make test     # tests for .tad/ (the engine) and for kit/guards
    make verify   # data valid and canonical, pages fresh: what CI runs
    make rst      # every reStructuredText file is valid

If ``.tad/`` is not a git subrepo (``.tad/.gitrepo`` is missing) run ``./bin/adopt-engine.sh`` once. To pull engine updates: ``git subrepo pull .tad -m "chore(tad): pull engine update"``
(always with ``-m`` and a Conventional Commits message).

Layout
------

- ``kit/AGENT-INSTRUCTIONS.rst``: the document handed to an agent (prose).
- ``playbook/*.rst``: the chapters (prose).
- ``kit/guards/``, ``kit/scripts/``: reusable code, with tests (``make test``).
- ``data/schema.sql``, ``data/load.sql``, ``data/<table>.json``: the data (JSON lines despite the extension). Change it with SQL, never by hand.
- ``checks/*.sql``: invariants; each query must return no rows.
- ``docs/*.rst``: rendered pages. ``make render`` only.
- ``.tad/``: the engine. Do not hand-edit it: change it in ``tad-engine`` and pull.

Rules for the data
------------------

1. Never hand-edit ``data/*.json`` or anything in ``docs/``. Change data through SQL: ``make sql Q="UPDATE ...; SELECT ..."``. Then ``make render``.
2. Finish with ``make canon`` (``make sql`` does it for you). DuckDB must write the final bytes.
3. No BLOB columns; no foreign keys (put integrity in ``checks/*.sql``); do not change DuckDB session settings.
4. Every id in every table shares one namespace (``checks/01_ids_unique_across_tables.sql``).
5. A value may use the Markdown inline subset (code, links, bold, emphasis); the engine converts it for reStructuredText.
6. Add a **practice** as a ``concepts`` row with the *what* and the *why*, relate it to what it needs or extends in ``relations``, cite it in ``concept_sources``, and record any decision about it
   in ``session_log`` with what was considered and rejected.

Output format
-------------

This repository renders reStructuredText: ``export DOCS_FORMAT ?= rst`` in the ``Makefile``. ``DOCS_FORMAT=md,rst make render`` writes both if you need to compare.

Commits
-------

Conventional Commits, linted on the pull request; squash merges. See ``CONTRIBUTING.rst``.
