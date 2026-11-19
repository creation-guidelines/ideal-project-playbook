<!-- Generated from data/ by tad. Do not edit by hand. -->

# Backlog

<a id="second-project"></a>
### Apply the playbook to a second, different project and record what does not transfer

Status
: open

Note
: Everything here was learned on one project. The honest test is a second one in another language.

Opened
: 2026-11-03


<a id="python-guards"></a>
### Check the Python guard kit against a real Python project

Status
: open

Note
: The kit's Python guards are tested on small fixtures here, not yet on a project of size.

Opened
: 2026-11-03


<a id="typescript-guards"></a>
### Port the guard kit to TypeScript

Status
: open

Note
: Outline from TSDoc first sentences; the ratchet and the findability ranker are language-neutral.

Opened
: 2026-11-03


<a id="go-guards"></a>
### Port the guard kit to Go

Status
: open

Note
: Outline from package and function doc comments.

Opened
: 2026-11-03


<a id="sphinx-site"></a>
### Publish the playbook as a Sphinx site

Status
: open

Note
: The .rst files are valid for Sphinx as written; the generated pages use plain links, so a Sphinx build needs a small index.

Opened
: 2026-11-03


<a id="site-builder-in-the-engine"></a>
### Move the site builder into tad-engine

Status
: open

Note
: Every repository that renders reStructuredText from the template needs the same site; the builder belongs in the engine so that it is pulled, not copied. It needs the page list and navigation to come from the rendered pages rather than from this repository's fixed list.

Opened
: 2026-11-03


<a id="retire-own-python"></a>
### Measure what uses the playbook's Python, port the live files to Rust, retire the rest

Status
: open

Note
: Practice 21: no Python of our own. kit/guards/*.py, kit/rust/*.py, kit/scripts/*.py and tools/*.py (build_site, check_paths, check_rst) run in make test, rst and site. First measure what still calls each file (Makefile, CI, kit templates), then port the live ones to Rust (rust-script for a single file, a crate where it repeats) and delete the rest with their tests. Shell only for true one-off glue that strings commands together: the author, 2026-11-19, 'shell is even worse than python for any scripts that isnt a one off glue'.

About
: licences

Opened
: 2026-11-19
