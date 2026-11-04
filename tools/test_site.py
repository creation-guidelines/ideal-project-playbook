#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Tests for tools/build_site.py. Plain asserts, no framework: ``python3 tools/test_site.py``."""
import importlib.util
import os
import re
import sys
import tempfile
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("build_site", os.path.join(HERE, "build_site.py"))
site = importlib.util.module_from_spec(spec)
spec.loader.exec_module(site)


def project(files):
    root = tempfile.mkdtemp()
    for path, text in files.items():
        full = os.path.join(root, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, "w", encoding="utf-8").write(text)
    site.ROOT = root
    return root


def built(files):
    project(files)
    out = tempfile.mkdtemp()
    result = site.build(out)
    return out, result


def read(out, path):
    return open(os.path.join(out, path), encoding="utf-8").read()


FRONT = "ideal-project-playbook\n======================\n\nSee `the idea <playbook/idea.rst#why>`__ and `Elsewhere <https://example.com/x.rst>`__.\n"
IDEA = "The idea\n========\n\n.. _why:\n\nWhy\n---\n\nBack to `the front <../README.rst>`__.\n"


def test_each_rst_becomes_a_page_and_the_readme_is_the_front_page():
    out, (pages, links, broken) = built({"README.rst": FRONT, "playbook/idea.rst": IDEA})
    assert pages == 2 and broken == []
    assert os.path.exists(os.path.join(out, "index.html")) and os.path.exists(os.path.join(out, "playbook", "idea.html"))
    assert os.path.exists(os.path.join(out, "style.css")) and os.path.exists(os.path.join(out, ".nojekyll"))


def test_links_between_pages_are_rewritten_relative_to_the_page_they_are_on():
    out, _ = built({"README.rst": FRONT, "playbook/idea.rst": IDEA})
    assert 'href="playbook/idea.html#why"' in read(out, "index.html")
    assert 'href="../index.html"' in read(out, "playbook/idea.html")


def test_an_external_link_is_left_alone_even_if_it_ends_in_rst():
    out, _ = built({"README.rst": FRONT, "playbook/idea.rst": IDEA})
    assert 'href="https://example.com/x.rst"' in read(out, "index.html")


def test_a_link_to_a_file_that_is_not_a_page_stops_the_build():
    project({"README.rst": "Home\n====\n\nSee `missing <nope.rst>`__.\n"})
    try:
        site.build(tempfile.mkdtemp())
    except SystemExit as stop:
        assert "nope.rst" in str(stop) and "not a page" in str(stop), stop
        return
    raise AssertionError("a broken link should have stopped the build")


def test_a_link_to_an_anchor_that_is_not_on_the_page_is_reported():
    _, (_, _, broken) = built({"README.rst": "Home\n====\n\nSee `x <idea.rst#nowhere>`__.\n", "idea.rst": "Idea\n====\n\ntext\n"})
    assert len(broken) == 1 and "idea.rst#nowhere" in broken[0], broken


def test_a_rst_error_stops_the_build_instead_of_shipping_a_broken_page():
    project({"README.rst": "Home\n====\n\n.. nosuchdirective::\n\ntext\n"})
    try:
        site.build(tempfile.mkdtemp())
    except Exception:
        return
    raise AssertionError("an unknown directive should have failed the build")


def test_the_front_page_title_is_not_doubled_and_the_navigation_lists_only_pages_that_exist():
    out, _ = built({"README.rst": FRONT.replace("ideal-project-playbook\n======================", "ideal-project-playbook\n======================"), "playbook/idea.rst": IDEA})
    front = read(out, "index.html")
    assert "<title>ideal-project-playbook</title>" in front, re.search(r"<title>.*?</title>", front).group(0)
    assert "docs/concepts.html" not in front, "no link to a page that is not there"
    assert "<title>The idea - ideal-project-playbook</title>" in read(out, "playbook/idea.html")


TESTS = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]

if __name__ == "__main__":
    failed = 0
    for t in TESTS:
        try:
            t()
            print("ok  ", t.__name__)
        except Exception:
            failed += 1
            print("FAIL", t.__name__)
            traceback.print_exc()
    print(f"{len(TESTS) - failed}/{len(TESTS)} passed")
    sys.exit(1 if failed else 0)
