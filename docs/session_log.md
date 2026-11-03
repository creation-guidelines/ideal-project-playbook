<!-- Generated from data/ by .tad/tools/render.py. Do not edit by hand. -->

# Session Log

<a id="duckdb-jsonl-storage"></a>
### Chose DuckDB + JSONL as the storage format

Entry date
: 2026-09-21

Done
: Adopted DuckDB's EXPORT DATABASE layout (schema.sql, load.sql, one JSON-lines file per table) as the on-disk format for text-as-data, edited via SQL and canonicalized back to git-diffable files.

Considered
: Doltgres, Dolt, gitsheets, GlueSQL, SQLite + sqlite-diffable.

Rejected
: Doltgres/Dolt hide data history behind a non-file-visible git ref, unreadable in a PR. gitsheets has no SQL or joins. GlueSQL reinvents a SQL engine with no ALTER TABLE support, more machinery than the job needed.

---


<a id="extract-template-from-working-repo"></a>
### Extracted a template from a working repo, not designed one first

Entry date
: 2026-09-21

Done
: Built the real content repo (software-engineering-canon, from design-canon) first, then extracted the proven tooling into this template once it had actually been used.

Considered
: Designing the template repo first, in the abstract.

Rejected
: An abstraction is only right once it has met a real case - designing the template first risked encoding assumptions that would not survive contact with real content.

---


<a id="switch-subtree-to-subrepo"></a>
### Switched .tad/ from git subtree to git subrepo

Entry date
: 2026-09-22

Done
: Vendored .tad/ as a git subrepo instead of a git subtree, after testing both against the same real engine update.

Considered
: Continuing with git subtree (the original choice).

Rejected
: subrepo writes one commit per sync instead of subtree's two, and tracks the pinned commit explicitly in .gitrepo instead of a squash-commit trailer subtree buries in commit history.

---


<a id="decline-to-fork-git-subrepo"></a>
### Declined to fork git-subrepo for custom commit messages

Entry date
: 2026-09-22

Done
: Verified directly that git subrepo clone/pull/push already accept -m/--message and it fully replaces the tool's auto-generated message, with .gitrepo (not the commit message) tracking state.

Considered
: Forking ingydotnet/git-subrepo and patching it to prompt for a commit message.

Rejected
: Unnecessary: the flag already existed. Forking would mean taking on indefinite maintenance of a bash-script fork for a feature that shipped already.

---


<a id="tag-dist-for-pinning"></a>
### Tagged the dist branch itself to enable version pinning

Entry date
: 2026-09-22

Done
: Added a release.yml step that tags dist as dist/vX.Y.Z right after release-please tags main, giving consumers a pinned, engine-only ref instead of the moving dist branch.

Considered
: Reusing release-please's own vX.Y.Z tag on main for pinning.

Rejected
: That tag's tree contains tad-engine's own governance files (commitlint config, CHANGELOG.md), exactly the clutter dist exists to avoid; a same-named tag on dist would also collide with it (git's tag namespace is repo-wide) - found by actually running a release, not by review, and fixed by namespacing as dist/vX.Y.Z.

---


<a id="backlog-as-a-table"></a>
### Adopted a backlog table as a standing convention

Entry date
: 2026-09-22

Done
: Every project built this way keeps a backlog table (status: open/in-progress/done), rendered to its own page the same as any other content.

Considered
: A separate issue tracker, or a free-form Markdown TODO file.

Rejected
: Either breaks the property the rest of the system relies on: everything queryable, versioned, and diffable in the same place, not split across tools.

---


<a id="rfc-like-minimal-style"></a>
### Switched the Pages presentation to an RFC-like minimal style

Entry date
: 2026-09-22

Done
: Replaced bold "**Field:** value" lines in render.py with kramdown definition lists (Term / : Definition), and replaced the never-actually-committed jekyll-theme-primer setup with a custom minimal layout and stylesheet: monospace, headings sized close to body text, links underlined with no color, structure carried by indentation rather than font-size or bold. Applied to text-as-data-template only for now, via the normal engine-pull path - other repos keep their current style until they choose to pull.

Considered
: Keeping jekyll-theme-primer and just trimming it with overrides.

Rejected
: Discovered while doing this that docs/_config.yml had never actually been committed to this repo at all - the site had been running on GitHub Pages' unstyled Jekyll default this whole time, not a deliberate theme choice.
