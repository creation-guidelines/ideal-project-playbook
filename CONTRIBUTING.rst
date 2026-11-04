Contributing
============

Commit messages: Conventional Commits
-------------------------------------

Every commit on a pull request is linted (``commitlint``) against `Conventional Commits <https://www.conventionalcommits.org/>`__: ``type(scope): subject``. It is not decorative:
`release-please <.github/workflows/release.yml>`__ reads these commits to decide the next version and to write ``CHANGELOG.md``, so the type has a real effect.

``feat``
    New content: a practice, a chapter, a script, a table, a capability. Minor version.
``fix``
    A correction: a wrong statement, a wrong constraint, a bug in a script or in ``.tad/``. Patch.
``docs``
    Hand-written documents only (README, this file, AGENTS, the chapters). Not the generated ``docs/`` pages, which travel with the ``feat`` or ``fix`` that changed the data.
``refactor``, ``chore``, ``ci``, ``test``
    Reshaping with no change in content; housekeeping; workflow changes; tests only. No bump.

A breaking change (a schema change that other consumers of this data would have to react to) adds ``!`` after the type or scope, or a ``BREAKING CHANGE:`` footer.

The scope is optional. This repository's convention is to name the part that changed: ``data``, ``schema``, ``playbook``, ``kit``, ``tools``, ``checks``, ``ci``. For example::

    feat(data): add a practice about reading the documentation of a switch
    docs(playbook): the lessons chapter says what each mistake taught
    fix(kit): the ratchet reports a file that is not in the recorded debts
    feat(kit): a Go outline extractor

Workflow
--------

See ``AGENTS.rst``. In short: change data through SQL, never hand-edit ``data/*.json`` or ``docs/``; keep the hand-written ``.rst`` valid (``make rst``); finish with ``make verify`` before opening a
pull request; squash-merge.
