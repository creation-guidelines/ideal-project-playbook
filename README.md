# text-as-data-template

A GitHub template for keeping a small dataset as plain, versioned files: SQL schema, JSON-lines
data, a Markdown site rendered from it, and CI that enforces both stay valid and canonical.

**Use this template** (the button above, or `gh repo create --template creation-guidelines/text-as-data-template`)
to start a new content repo, then run `./bin/adopt-engine.sh` once - GitHub's template generation
gives you a fresh, historyless copy of `.tad/`, not a `git`-connected one, so this one-time step is
what makes `git subrepo pull` (see [`.tad/README.md`](.tad/README.md)) work from then on; it needs
[`git-subrepo`](https://github.com/ingydotnet/git-subrepo) installed, which the script checks for.
The example content in `data/` and `checks/` is a placeholder - replace it with your own schema and
delete the `EXAMPLE:` rows. The example includes two standing tables every project built this way
should keep, alongside its actual content:
- `backlog` (status: open / in-progress / done, optionally linked to a concept via `relations`) -
  rendered to [`docs/backlog.md`](docs/backlog.md) here.
- `session_log` (one row per significant decision: what was done, what was considered, what was
  rejected and why) - rendered to [`docs/session_log.md`](docs/session_log.md) here, and, in this
  repo, populated with the real decisions behind this template and its engine (also home to
  [`tad-engine`](https://github.com/creation-guidelines/tad-engine)'s own backlog, since that repo
  has no `data/` of its own to keep one in).

- **Read the example site:** published to GitHub Pages once you enable it (Settings -> Pages -> Deploy from a branch -> `main` / `/docs`).
- **Working on it (humans or agents):** read [`AGENTS.md`](AGENTS.md), run `make setup`, then `make verify`.
- **Commit convention and how releases work:** [`CONTRIBUTING.md`](CONTRIBUTING.md).

## How it works
`data/` is the source of truth: a SQL schema (`schema.sql`), the load statements DuckDB writes
(`load.sql`), and one JSON-lines file per table. DuckDB loads it in memory, SQL edits it, and it
is written back in canonical form, so a one-row change is a one-line diff. `checks/*.sql` holds
invariants you write for your own schema (ids unique, relations resolve, and so on). CI runs
`make verify`: the data must be valid, canonical, and the rendered `docs/` must be current.

All of the reusable machinery lives in [`.tad/`](.tad/README.md), vendored as a `git subrepo`
from [creation-guidelines/tad-engine](https://github.com/creation-guidelines/tad-engine) - see that
file for how to pull engine updates, and fix or extend the engine itself over there, not here
(a local edit to `.tad/` is what turns the next pull into a merge conflict).

## Output format
Pages render as Markdown by default; `DOCS_FORMAT=rst make render` renders reStructuredText, and `DOCS_FORMAT=md,rst`
both. The data is written once. See [`AGENTS.md`](AGENTS.md) and [`.tad/README.md`](.tad/README.md).

## Releases
Commits follow [Conventional Commits](https://www.conventionalcommits.org/) and are linted on
every PR. [release-please](https://github.com/googleapis/release-please) reads them on `main` and
opens a release PR with an updated `CHANGELOG.md`; merging it tags a release. See
[`CONTRIBUTING.md`](CONTRIBUTING.md) for the type/scope convention.

## Status
No license has been chosen. Add one appropriate to your content before using this for anything
you intend other people to reuse.
