#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 grenudi
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Tests for screens.py, against a tiny terminal program written here. Plain asserts: ``python3 kit/scripts/test_screens.py``. Needs pyte (skipped loudly without it)."""
import importlib.util
import os
import sys
import tempfile
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("screens", os.path.join(HERE, "screens.py"))
screens = importlib.util.module_from_spec(spec)
spec.loader.exec_module(screens)

PROGRAM = r'''
import sys, tty, termios
fd = sys.stdin.fileno(); old = termios.tcgetattr(fd); tty.setraw(fd)
def draw(s): sys.stdout.write("\x1b[2J\x1b[H" + s); sys.stdout.flush()
draw("ONE\r\nsize " + str(__import__("shutil").get_terminal_size()))
try:
    buf = b""
    while True:
        c = sys.stdin.buffer.read1(8)
        if c == b"2": draw("TWO \u250c\u2500\u2510")
        elif c == b"\r": draw("ENTER")
        elif c == b"\x1b[B": draw("DOWN")
        elif c == b"q": break
finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old)
'''


def program():
    path = os.path.join(tempfile.mkdtemp(), "tui.py")
    open(path, "w").write(PROGRAM)
    return [sys.executable, path]


def have_pyte():
    try:
        import pyte  # noqa: F401
        return True
    except ImportError:
        print("    (skipped: pyte is not installed)")
        return False


def test_the_first_screen_and_the_screen_after_each_key_are_what_the_program_drew():
    if not have_pyte():
        return
    t = screens.Terminal(program(), 60, 12)
    try:
        t.settle(1.0)
        assert t.text().startswith("ONE"), t.text()
        assert "size" in t.text() and "60" in t.text() and "12" in t.text(), "the program sees the size it was given: " + t.text()
        t.press("2", 0.4)
        assert t.text() == "TWO \u250c\u2500\u2510", repr(t.text())
        t.press("enter", 0.4)
        assert t.text() == "ENTER"
        t.press("down", 0.4)
        assert t.text() == "DOWN"
    finally:
        t.close()


def test_a_key_is_a_character_or_a_name_and_anything_else_is_refused():
    assert screens.key_bytes("a") == b"a" and screens.key_bytes("enter") == b"\r" and screens.key_bytes("up") == b"\x1b[A"
    try:
        screens.key_bytes("page-down")
    except SystemExit as stop:
        assert "unknown key" in str(stop) and "enter" in str(stop)
        return
    raise AssertionError("an unknown key should be refused")


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
