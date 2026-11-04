The kit
=======

Everything here was extracted from a project where it was used for real, and each piece has tests (``make test``). Copy what you need; the ``<placeholders>`` and the CONFIG blocks are the parts to change.

``kit/AGENT-INSTRUCTIONS.rst``
    The document to give an agent.

Guards: rules as tests (``kit/guards/``)
    ``kit/guards/ratchet.py`` (debts as data that may only shrink), ``kit/guards/outline.py`` (every module's first sentence), ``kit/guards/findability.py`` (the outline answers real
    questions), ``kit/guards/rules.py`` (the catalogue of guards as functions: file size, entry files, shared purposes, pattern jargon, purity by role, hand-spelled plurals, retired
    words checked by a lexer) and ``kit/guards/architecture.py`` (all of them wired up: this repository's own guard, and the one to copy). ``kit/guards/self-questions.json`` is a worked
    example of the findability questions.

Automation (``kit/scripts/``)
    ``kit/scripts/ship.py`` (push, pull request, CI, merge, release when the policy says, verify; stateless and resumable) with ``kit/scripts/test_ship.py``; ``kit/scripts/gate.sh`` (the fast gate);
    ``kit/scripts/golden-output.sh`` (pin what the program prints); ``kit/scripts/screens.py`` (look at a terminal program's screens through a pseudo-terminal);
    ``kit/scripts/structure-metrics.py`` (the shape of the code against an earlier release); ``kit/scripts/find-duplicates.py`` (repeated code, and with ``--near`` the same shape under other
    names); ``kit/scripts/sample-modules.py`` (seeded random modules to read as a stranger); ``kit/scripts/ci-timings.py`` (what CI costs).

The files a project starts with (``kit/templates/``)
    ``kit/templates/AGENTS.template.rst``, ``kit/templates/the-idea.template.rst``, ``kit/templates/development-log.template.rst``, ``kit/templates/backlog.template.rst``,
    ``kit/templates/pull-request-body.template.md`` and ``kit/templates/findability-questions.example.json``.

CI and releases (``kit/ci/``)
    ``kit/ci/ci.template.yml`` (the measured levers: a timeout on every job, a job that narrows what a change needs, the cache saved only from main, a prebuilt dependency checker),
    ``kit/ci/pr-title.template.yml``, ``kit/ci/release-plz.template.toml`` (releases are batched) and ``kit/ci/deny.template.toml`` (a dependency policy that was proven against a known-bad
    project).

Tools that need a lexer (``kit/rust/``)
    ``kit/rust/split-module.py`` (splits a module by purpose and refuses to write unless every comment survives) and ``kit/rust/rename-identifier.py`` (renames identifier tokens only, follows
    string interpolation, and checks that no string literal changed). Rust-specific; the *contract* is what to copy to another language.

``kit/requirements.txt``
    ``pyte``, for ``kit/scripts/screens.py``.
