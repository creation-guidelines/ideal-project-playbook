How close are we?
=================

A direction needs a way to say how far along it you are, in numbers a person can check and in plain words a person can feel.

The numbers
-----------

``structure-metrics`` compares the code now with each earlier release. On ``snapall``, from release 0.26.0 (where this work began) to the state described in this playbook:

- source files: 178 to 244 (big things were split by purpose)
- median file: 100 lines to 80
- files over 300 lines: 5 to 1; files huddled just under the limit (250 to 299): 14 to 8
- entry files over 120 lines: 2 to 0
- functions over 60 lines: 29 to 25 (the longest left is a deliberate request table)
- prints outside the presenter: 15 to 0
- bare boolean parameters in commands: 34 to 1 (the remaining one is the boundary that turns a flag into a noun)
- fields of the window's state: 26 to 14
- modules whose first sentence uses pattern jargon: 2 to 0
- hand-spelled plurals: 23 to 0
- the findability test: 52 questions; all 52 answers within the first three results, about 37 first
- the guard debts: a single entry left, the table of every flag (498 lines)
- tests: 618; releases: from 0.27.3 to 0.34.13 over about a week, each verified

The numbers are not the point and can be gamed: a splitter can lower a line count without making anything clearer. They exist to catch backsliding and to give the plain-word report something to be about.

The plain words
---------------

A report on closeness says, per layer, how close it is and why, and is honest about the rest. At the point of this playbook:

**Closest:** the commands. Every command is a short story, the request table reads as plain English, and the words a person reads (counts, plurals, failures, "nothing here yet") each live in one place.
The core is folders named for what the program is for.

**Close:** the window, and, surprisingly, the adapters. The window is split into screens and questions that each own their state and their drawing, and speaks through the same words as the command line.
The adapters had been guessed to be the least like the ideal; read by their first lines, each says what it is for and their functions are short.

**Least close, said plainly:** the drawing code, which is long because drawing is; the table of every flag, which reads as a table and whose sections now say what they are for; and the words of the underlying
tools, which still appear in a few places that other programs read (a published contract, an audit log) because renaming them would break those programs.

How to write it for a person
----------------------------

Use the shape in ``kit/AGENT-INSTRUCTIONS.rst``: what changed, how much closer, what went wrong, next. Keep it short. Say the one thing the person would most want to know first. Say what you could not
check ("none of this has run on your own machine yet"). If you guessed, say that.
