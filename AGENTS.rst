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

1. **Never hand-edit** ``data/*.json`` **or anything in** ``docs/``. Change data through SQL: ``make sql Q="UPDATE ...; SELECT ..."``. Then ``make render``.
2. **Always finish with** ``make canon`` (``make sql`` does it for you). DuckDB must write the final bytes, or CI fails on a non-canonical diff; a plain ``mlr``
   pass rewrites every line with different spacing.
3. **No BLOB columns.** They corrupt on the first JSON round trip. Use base64 ``VARCHAR``.
4. **Do not change DuckDB session settings** such as ``preserve_insertion_order``: row order is what keeps a diff at one line per changed row.
5. **No foreign keys.** They block nearly every ``ALTER TABLE`` on the referenced table. Put integrity in ``checks/*.sql`` instead: each query must return no
   rows, and ``make checks`` runs them all.
6. **Every id in every table shares one namespace** (``checks/01_ids_unique_across_tables.sql``), and both ends of every relation must exist
   (``checks/02_relations_resolve.sql``).
7. **A factual claim needs a source.** Every practice cites at least one, through ``concept_sources``
   (``checks/03_every_practice_cites_a_source.sql``). A practice learned on a project cites where it was learned; one taken from a reference cites the reference.
8. **Do not bump DuckDB** (or any dependency of ``.tad/``) here: the engine pins it and its tests run against the pin, and a hand edit of ``.tad/`` turns the next
   ``git subrepo pull`` into a conflict. Bump it in ``tad-engine`` and pull.
9. A value may use the Markdown inline subset (code, links, bold, emphasis); the engine converts it for reStructuredText.
10. **Add a practice** as a ``concepts`` row with the *what* and the *why*, relate it to what it needs or extends in ``relations``, cite it in ``concept_sources``,
    and record any decision about it in ``session_log`` with what was considered and rejected. Record each working session in ``session_log`` the same day, with
    the date from ``date``.

Recipes
-------

Add or change content::

    make sql Q="INSERT INTO concepts VALUES ('an-id','Name','What it is, and why.',['tag'])"
    make sql Q="INSERT INTO concept_sources VALUES ('an-id','snapall-log')"
    make sql Q="UPDATE concepts SET statement = '...' WHERE id = 'an-id'"
    make render && make verify

A schema change DuckDB allows (add a column with a default, rename a column, drop a non-key column, change a non-key type, ``SET NOT NULL``, rename a table)::

    make sql Q="ALTER TABLE concepts ADD COLUMN maturity VARCHAR DEFAULT 'stable'"

A schema change DuckDB refuses (add a column with constraints, ``ADD CONSTRAINT CHECK``, drop or retype a key column)::

    # 1. edit the CREATE line in data/schema.sql by hand
    # 2. give every data line the new key (Miller, in place):
    mlr -I --ijsonl --ojsonl put '$weight = 1' data/concepts.json
    # 3. validate and normalise; a wrong edit fails loudly here and leaves the files untouched
    make canon && make render && make verify

Rename a field across all lines: ``mlr -I --ijsonl --ojsonl rename old,new data/<table>.json``, make the same change in ``data/schema.sql``, then ``make canon``
(forgetting the schema is caught by ``make check``).

Build and look at the site: ``make site`` writes ``_site/``. Look at the pages in a browser before relying on them: a structural check cannot see that a page looks wrong.

Why it is built this way
------------------------

- DuckDB is the engine, in memory; no database file is committed. ``IMPORT DATABASE`` loads ``data/`` and ``EXPORT DATABASE ... (FORMAT json)`` writes it back byte-stably,
  so a change to one row is a one-line diff.
- ``dc.py check`` exists because DuckDB's ``COPY FROM json`` silently drops unknown keys and fills missing nullable columns with NULL.
- The renderer is schema-agnostic: it detects a relations table and a sources table by their *shape*, not their name, so a new schema needs no configuration.
- GitHub Pages does not render reStructuredText, so ``tools/build_site.py`` does, with docutils alone, and fails on any broken link or anchor.
- The findings and measurements behind these rules were made on the first content repository,
  `software-engineering-canon <https://github.com/creation-guidelines/software-engineering-canon>`__, and the engine's own tests.

Output format
-------------

This repository renders reStructuredText: ``export DOCS_FORMAT ?= rst`` in the ``Makefile``. ``DOCS_FORMAT=md,rst make render`` writes both if you need to compare.

Commits
-------

Conventional Commits, linted on the pull request; squash merges. See ``CONTRIBUTING.rst``.
