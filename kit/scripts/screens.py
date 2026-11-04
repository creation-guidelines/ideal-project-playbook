#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 grenudi
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Look at the screens of a terminal program as a person would: run it in a pseudo-terminal, press keys, and print what is on the screen after each.

    screens.py [--size COLSxROWS] [--wait SECONDS] [--keys KEY,KEY,...] -- COMMAND [ARGS...]

Reading a program's code finds what is wrong with the code; only using the program finds what is wrong with what it says. For a command line that is
running it and reading the output. For a terminal UI it needs a terminal: this one runs the program in a pseudo-terminal of the given size (default
100x30), feeds the output to a terminal emulator (pyte), presses each key in turn, waits for the screen to settle, and prints it. A key is a single
character, or one of: enter, esc, tab, space, backspace, up, down, left, right, ctrl-c, ctrl-d.

    screens.py --keys 2,3,?,q -- ./target/debug/myapp tui        the first screen, then the screen after each key

Needs ``pip install pyte``. Output uses box-drawing characters: do not cut it with a byte-oriented tool (``cut``), or the stream is no longer UTF-8.
"""
import fcntl
import os
import pty
import select
import signal
import struct
import sys
import termios
import time

KEYS = {"enter": b"\r", "esc": b"\x1b", "tab": b"\t", "space": b" ", "backspace": b"\x7f", "ctrl-c": b"\x03", "ctrl-d": b"\x04",
        "up": b"\x1b[A", "down": b"\x1b[B", "right": b"\x1b[C", "left": b"\x1b[D"}


def key_bytes(name):
    if name in KEYS:
        return KEYS[name]
    if len(name) == 1:
        return name.encode()
    raise SystemExit(f"screens.py: unknown key {name!r}; a character or one of: {', '.join(KEYS)}")


class Terminal:
    """A program running in a pseudo-terminal, and the screen it has drawn."""

    def __init__(self, command, cols=100, rows=30, env=None):
        import pyte
        self.screen = pyte.Screen(cols, rows)
        self.stream = pyte.ByteStream(self.screen)
        self.pid, self.fd = pty.fork()
        if self.pid == 0:
            os.environ.update(env or {})
            os.environ.setdefault("TERM", "xterm-256color")
            os.execvp(command[0], command)
        fcntl.ioctl(self.fd, termios.TIOCSWINSZ, struct.pack("HHHH", rows, cols, 0, 0))

    def settle(self, wait=0.6, patience=4.0):
        """Read until the program has been quiet for ``wait`` seconds (or ``patience`` in all)."""
        end, quiet_since = time.time() + patience, time.time()
        while time.time() < end and time.time() - quiet_since < wait:
            ready, _, _ = select.select([self.fd], [], [], 0.05)
            if ready:
                try:
                    data = os.read(self.fd, 65536)
                except OSError:
                    return
                if not data:
                    return
                self.stream.feed(data)
                quiet_since = time.time()

    def press(self, key, wait=0.6):
        os.write(self.fd, key_bytes(key))
        self.settle(wait)

    def text(self):
        lines = [line.rstrip() for line in self.screen.display]
        while lines and not lines[-1]:
            lines.pop()
        return "\n".join(lines)

    def close(self):
        for sig in (signal.SIGTERM, signal.SIGKILL):
            try:
                os.kill(self.pid, sig)
                time.sleep(0.05)
                os.waitpid(self.pid, os.WNOHANG)
            except (ProcessLookupError, ChildProcessError):
                break


def main(argv):
    if "--" not in argv:
        sys.exit(__doc__)
    split = argv.index("--")
    options, command = argv[:split], argv[split + 1:]
    value = lambda name, default: options[options.index(name) + 1] if name in options else default
    cols, rows = (int(n) for n in value("--size", "100x30").split("x"))
    wait = float(value("--wait", "0.6"))
    keys = [k for k in value("--keys", "").split(",") if k]
    terminal = Terminal(command, cols, rows)
    try:
        terminal.settle(max(wait, 1.5))
        print("=== the first screen ===")
        print(terminal.text())
        for key in keys:
            terminal.press(key, wait)
            print(f"\n=== after {key} ===")
            print(terminal.text())
    finally:
        terminal.close()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
