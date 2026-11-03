# AGENTS.md - how to work in this repository

This repo is a small versioned "database" kept as plain files. The data lives as JSON-lines plus
a SQL schema; SQL edits it; CI enforces that it stays valid, canonical, and rendered. **Work on
the content. The system in `.tad/` is generic and should rarely need to change.**

## Setup (once per session)
```
make setup    # pins DuckDB (pip) and Miller (mlr) to the versions .tad/bootstrap.sh installs
make test     # tests for .tad/ itself
make verify   # exactly what CI runs
```

If `.tad/` is a plain folder rather than a git subrepo (check for `.tad/.gitrepo` - if it's
missing, it's plain), this repo was likely just generated from the template and needs
`./bin/adopt-engine.sh` run once, before any other commit touches `.tad/`. See
[`.tad/README.md`](.tad/README.md) for what that does and how to pull engine updates afterward.

## Layout
| Path | What | Who writes it |
|---|---|---|
| `data/schema.sql` | DDL, one `CREATE` per table | you, by SQL `ALTER` or by hand (see below) |
| `data/load.sql` | `COPY` statements | DuckDB only |
| `data/<table>.json` | one JSON object per line (JSONL despite the extension) | DuckDB only |
| `checks/*.sql` | invariants: each query must return **no rows** | you |
| `docs/*.md` (or `docs/*.rst`) | rendered pages, in the format `DOCS_FORMAT` names (published to GitHub Pages when Markdown) | `make render` only |
| `.tad/` | the reusable engine (generic, schema-agnostic) | rarely - see `.tad/README.md` |

## Rules
1. **Never hand-edit `data/*.json` or anything in `docs/`.** Change data through SQL: `make sql Q="UPDATE ...; SELECT ..."`. Then `make render`.
2. **Always finish with `make canon`** (`make sql` does this automatically). DuckDB must write the final bytes, or CI fails on a non-canonical diff. A plain `mlr` pass rewrites every line with different whitespace.
3. **No BLOB columns.** They corrupt on the first JSON round trip. Use base64 `VARCHAR`.
4. **Do not change DuckDB session settings** such as `preserve_insertion_order`; row order is what keeps diffs at one line per changed row.
5. **No foreign keys.** They block nearly every `ALTER TABLE` on the referenced table. Put referential integrity in `checks/*.sql` instead.
6. **Commits follow Conventional Commits** and are linted on the PR; see [`CONTRIBUTING.md`](CONTRIBUTING.md) for the type/scope convention this repo uses and why it matters (it drives the automated release and changelog).
7. **New or changed factual claims need a source**, if your schema has a sources-like table (columns `title`, `url`) - see `.tad/tools/render.py`'s docstring for the exact convention it detects.

## Output format
Pages are written as Markdown by default. `DOCS_FORMAT=rst make render` writes reStructuredText instead, and
`DOCS_FORMAT=md,rst` writes both. Set it once for the repository by changing the `?=` default in the `Makefile`
(`export DOCS_FORMAT ?= rst`), and delete the pages of the format you stopped using: CI checks that the pages in
`docs/` are exactly what the data renders to. The data is written once, in Markdown inline syntax (`code`,
`[text](url)`, `**bold**`, `*emphasis*`); the engine converts and escapes it for reStructuredText.

## Recipes
Add or change content:
```
make sql Q="INSERT INTO concepts VALUES ('id','Name','One-line statement.',[])"
make sql Q="UPDATE concepts SET statement = '...' WHERE id = 'example-one'"
make render && make verify
```
Schema change, when DuckDB allows it (add column with default, rename column, drop a non-key column, change a non-key type, `SET NOT NULL`, rename table):
```
make sql Q="ALTER TABLE concepts ADD COLUMN maturity VARCHAR DEFAULT 'stable'"
```
Schema change DuckDB refuses (add a column with constraints, `ADD CONSTRAINT CHECK`, drop or retype a key column):
```
# 1. edit the CREATE line in data/schema.sql by hand
# 2. give every data line the new key (Miller, in place):
mlr -I --ijsonl --ojsonl put '$weight = 1' data/concepts.json
# 3. validate and normalize; a wrong edit fails loudly here and leaves files untouched
make canon && make render && make verify
```
Rename a field across all lines: `mlr -I --ijsonl --ojsonl rename old,new data/<table>.json`, edit the same name in `data/schema.sql`, then `make canon`. Forgetting the schema edit is caught by `make check` (DuckDB itself would silently load NULLs).

## Why it is built this way
- DuckDB is the engine (in memory; no `.db` file is committed). `IMPORT DATABASE` loads `data/`, `EXPORT DATABASE ... (FORMAT json)` writes it back byte-stably.
- `.tad/tools/dc.py check` exists because DuckDB's `COPY FROM json` silently drops unknown keys and NULL-fills missing nullable columns.
- `.tad/tools/render.py` is schema-agnostic by detecting shapes (a relation table, a sources table) structurally, not by name, so it works on a fresh schema with no configuration.
- Findings and measurements behind these rules were made on a first content repo, [`creation-guidelines/software-engineering-canon`](https://github.com/creation-guidelines/software-engineering-canon), which this template was extracted from.
