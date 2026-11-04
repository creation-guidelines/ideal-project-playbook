The idea
========

One sentence
------------

**Every layer is the top of the layers beneath it.**

Imagine reading a program from the top. The first thing you meet says what the program is *for*, in
the words a person would use: take a snapshot, go back, protect an area. You can stop there and know
the program. Each step down answers one question, *how is that done?*, and it answers it using only
the words of the step beneath. Going back to a restore point is written as a handful of plain steps:
look at what would change, ask, begin, do it, end, show the result. Each of those steps is a word that
the layer below provides, and that layer is in turn written in words from the layer below it, until you
reach the places that touch the machine.

So you never hold the whole program in your head. You read a level, understand it, and open the next one
only if you want to know *how*.

The two faces
-------------

Every part has two faces.

The **upward face** is what the part is for and the words it offers to the layer above. It is the part's
first sentence, its name, its public vocabulary.

The **downward face** is the body: it is written *only* in the words of the layers beneath. If the body
needs a word that the layer below does not offer, the layer below is missing a noun, and the right fix is
to add the noun there, not to reach down through it.

A part that cannot be described this way is doing two jobs. The cure is always the same: split it, and name
the two things.

What it looks like in code
--------------------------

A command is a **story of named steps**. The restore-everything command in ``snapall`` reads:

- look at what putting the restore point back would change;
- ask, naming what will happen and what cannot be undone;
- begin the change (it is written down before it starts);
- do it, area by area;
- end the change, and record the way back;
- say what was done, and the exact command that undoes it.

Each step is one call to a word the layer below offers. The mechanism (disk, process, terminal) is not in
the story; it is in the words, and the words are in the layers below.

The program is a **stack of small languages**. The window and the command line are two ways in to the same
acts, and they speak the same sentences, written once, in the core. That is why the idea reaches the
*words a person reads* as well as the structure: a sentence is one more thing that lives in one place.

Names explain the program
-------------------------

Folders are named for what the program is *for*, not for how it is built. The core of ``snapall`` has
``going_back/``, ``keeping/``, ``protecting/``, ``taking/``, ``looking/``: a newcomer who reads the folder
listing learns what the program does. The layout it replaced was named for patterns (ports, adapters,
services), which tells you how it is built and nothing about what it is for.

A module's first sentence says what it is for, and says it without pattern words. "An in-memory adapter and
the contract every backend must satisfy" became "A stand-in for the snapshot tool that keeps everything in
memory, and the checks every real one must pass". The second sentence is for a person; the first was for the
architect who wrote it.

The measure: the stranger test
------------------------------

Someone who has never seen the code reads the first line of a part and can say what it is for, and is right.

It is the only measure of clarity that cannot be gamed by moving code around. A line budget is gamed by splitting
a file without making it clearer. A count of patterns is gamed by renaming. The stranger test is a person
(or an agent reading cold), and it can be turned into a test that runs on every change (see ``03-guards``,
*findability*).

What the idea is not
--------------------

- It is not a layering rule. Layers exist; the idea says what makes a layer good: that it is a small language, and
  that the layer above is written in it.
- It is not a size rule. Small files are a consequence, not the aim. A table that is long because the thing it
  lists is long (every flag of a command line) can be right, provided its sections say what they are for.
- It is not about the tool. In ``snapall`` the words of the underlying tools (*snapper*, *config*) live in the
  adapter that drives them and nowhere above it. Above, an area is an area.

Why it is worth the work
------------------------

Code written this way is cheap to change, because a change is local to the layer that owns the word. It is cheap to
*review*, because a pull request reads as a few sentences in a language the reviewer already knows. It is cheap to hand
to an agent, because the agent can open one level and be right about it. And it is pleasant to read, which is the
reason people keep a project alive.
