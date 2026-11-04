#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""build_site.py - the repository's reStructuredText as a small static site, for GitHub Pages.

    python3 tools/build_site.py [OUTPUT_DIR]        (default: _site)

GitHub Pages does not render reStructuredText, so this does, with docutils (the reference implementation), and nothing else: no theme,
no framework. Every ``.rst`` file becomes a page at the same path with ``.html`` (``README.rst`` becomes the front page), with a
navigation bar and one stylesheet. Links between pages are written in the sources as links to the ``.rst`` files, which is what makes
them work on GitHub's own file browser too; here they are rewritten to the pages. The build **fails** on a link to a file that is not a
page, and on a link to an anchor that is not on the page it points to, so the site cannot ship with a broken link. The instructions for
an agent are also copied as the raw ``.rst``, because that is the file you hand to one."""
import glob
import html
import os
import re
import shutil
import sys

from docutils.core import publish_parts

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAV = [("Home", "README.rst"), ("Agent instructions", "kit/AGENT-INSTRUCTIONS.rst"), ("Playbook", "playbook/index.rst"),
       ("Practices", "docs/concepts.rst"), ("Decisions", "docs/session_log.rst"), ("Sources", "docs/sources.rst"), ("Backlog", "docs/backlog.rst")]
RAW = ["kit/AGENT-INSTRUCTIONS.rst"]
SITE = "ideal-project-playbook"
REPOSITORY = "https://github.com/creation-guidelines/ideal-project-playbook"
LINK = re.compile(r'href="([^"#:]*?\.rst)(#[^"]*)?"')
ID = re.compile(r'\bid="([^"]+)"')

CSS = """\
:root { color-scheme: light dark; --fg: #1d1d1f; --bg: #fdfdfc; --dim: #6b6b70; --line: #deded9; --accent: #1a5fb4; --code: #f0f0ec; }
@media (prefers-color-scheme: dark) { :root { --fg: #e6e6e3; --bg: #17171a; --dim: #9a9aa1; --line: #2c2c31; --accent: #78aeed; --code: #222226; } }
html { font: 17px/1.6 Georgia, "Iowan Old Style", "Times New Roman", serif; }
body { margin: 0; color: var(--fg); background: var(--bg); }
nav { border-bottom: 1px solid var(--line); padding: .6rem 1rem; display: flex; flex-wrap: wrap; gap: .3rem 1.2rem; font: 15px/1.4 system-ui, sans-serif; }
nav a { color: var(--dim); text-decoration: none; } nav a:hover, nav a.here { color: var(--accent); }
main { max-width: 46rem; margin: 0 auto; padding: 1.5rem 1.2rem 4rem; }
h1, h2, h3 { line-height: 1.25; font-family: system-ui, sans-serif; } h1 { font-size: 1.9rem; } h2 { font-size: 1.4rem; margin-top: 2.2rem; border-bottom: 1px solid var(--line); padding-bottom: .2rem; }
h3 { font-size: 1.12rem; margin-top: 1.8rem; }
a { color: var(--accent); }
pre, code, tt { font: 14.5px/1.5 ui-monospace, "SF Mono", Menlo, Consolas, monospace; background: var(--code); border-radius: 4px; }
code, tt { padding: .1em .3em; } pre { padding: .8rem 1rem; overflow-x: auto; } pre code { padding: 0; background: none; }
blockquote { margin: 1rem 0; padding: .2rem 1.1rem; border-left: 3px solid var(--line); color: var(--dim); }
dl dt { font-family: system-ui, sans-serif; font-weight: 600; margin-top: .9rem; } dl dd { margin-left: 1.4rem; }
.contents, .topic { background: var(--code); border-radius: 6px; padding: .4rem 1.2rem; font: 15px/1.5 system-ui, sans-serif; } .topic-title { font-weight: 600; }
footer { max-width: 46rem; margin: 0 auto; padding: 1rem 1.2rem 3rem; border-top: 1px solid var(--line); color: var(--dim); font: 14px/1.5 system-ui, sans-serif; }
"""


def sources():
    found = [f for f in glob.glob(os.path.join(ROOT, "**", "*.rst"), recursive=True)
             if not any(part in f for part in ("/.git/", "/node_modules/", "/_site/", "/.tad/"))]
    return sorted(os.path.relpath(f, ROOT) for f in found)


def output_path(source):
    return "index.html" if source == "README.rst" else source[:-4] + ".html"


def relative(from_page, to_page):
    return os.path.relpath(to_page, os.path.dirname(from_page) or ".").replace(os.sep, "/")


def rewrite_links(body, source, pages, links):
    """Links to ``.rst`` files become links to the pages; each (page, target page, anchor) is kept to be checked."""
    def one(match):
        target = os.path.normpath(os.path.join(os.path.dirname(source), match.group(1))).replace(os.sep, "/")
        if target not in pages:
            raise SystemExit(f"{source}: links to {match.group(1)}, which is not a page of the site (the file must be a .rst file in the repository)")
        anchor = match.group(2) or ""
        links.append((source, target, anchor[1:]))
        return f'href="{relative(output_path(source), output_path(target))}{anchor}"'
    return LINK.sub(one, body)


def page(source, title, body, here):
    out = output_path(source)
    nav = "".join(f'<a href="{relative(out, output_path(path))}"{" class=here" if path == here else ""}>{html.escape(name)}</a>' for name, path in NAV if path in sources())
    raw = "".join(f' &middot; <a href="{relative(out, path)}">this page as plain .rst</a>' for path in RAW if path == source)
    return (f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<title>{html.escape(title if title == SITE else f"{title} - {SITE}")}</title><link rel="stylesheet" href="{relative(out, "style.css")}"></head>\n'
            f'<body><nav>{nav}</nav>\n<main>\n{body}\n</main>\n'
            f'<footer>Generated from the repository\'s reStructuredText &middot; <a href="{REPOSITORY}/blob/main/{source}">{html.escape(source)} on GitHub</a>{raw}</footer>\n</body></html>\n')


def build(out_dir):
    pages = set(sources())
    links, built = [], {}
    for source in sorted(pages):
        with open(os.path.join(ROOT, source), encoding="utf-8") as f:
            parts = publish_parts(f.read(), source_path=source, writer_name="html5",
                                  settings_overrides={"report_level": 2, "halt_level": 2, "syntax_highlight": "none", "embed_stylesheet": False,
                                                      "stylesheet_path": None, "file_insertion_enabled": False, "raw_enabled": False})
        body = rewrite_links(parts["html_body"], source, pages, links)
        built[source] = (parts["title"] or source, body)
    shutil.rmtree(out_dir, ignore_errors=True)
    for source, (title, body) in built.items():
        path = os.path.join(out_dir, output_path(source))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(page(source, title, body, source))
    for path in RAW:
        if path in pages:
            os.makedirs(os.path.dirname(os.path.join(out_dir, path)) or out_dir, exist_ok=True)
            shutil.copyfile(os.path.join(ROOT, path), os.path.join(out_dir, path))
    with open(os.path.join(out_dir, "style.css"), "w", encoding="utf-8") as f:
        f.write(CSS)
    open(os.path.join(out_dir, ".nojekyll"), "w").close()  # Pages must serve the files as they are
    ids = {source: set(ID.findall(built[source][1])) for source in built}
    broken = [f"{source}: links to {target}#{anchor}, which is not on that page" for source, target, anchor in links if anchor and anchor not in ids[target]]
    return len(built), len(links), broken


def main(argv):
    out_dir = os.path.abspath(argv[0] if argv else os.path.join(ROOT, "_site"))
    pages, links, broken = build(out_dir)
    for line in broken:
        print("BROKEN", line)
    print(f"{pages} pages, {links} links between them checked, {len(broken)} broken -> {os.path.relpath(out_dir, ROOT)}/")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
