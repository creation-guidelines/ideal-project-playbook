CI and releases
===============

Measure the CI before changing it
---------------------------------

Collect, over several recent runs: median wall time, job-minutes (total runner time, which is what costs money), and the slowest jobs
and steps. ``ci-timings.py --runs 8 --steps`` does it.

On ``snapall`` the baseline over eight runs was a median of **193 seconds** wall time and **20.0 job-minutes** per full run. The slowest
single step was a security audit action that compiled its own tool from source: **181 seconds**.

What paid
---------

- **A prebuilt tool instead of compiling it.** The audit became a prebuilt ``cargo-deny`` with its policy written down in ``deny.toml``
  (vulnerabilities fail; unmaintained fails only for direct dependencies; yanked warns). Before replacing the old audit, the new policy
  was proven locally against a scratch project that depends on a version with a known advisory: it failed there and passed on the repository.
- **A timeout on every job** (29 jobs in 7 workflows), so a hung job is a failure in minutes, not hours.
- **The cache saved only from the main branch**, so pull requests read it and never write a competing one.
- **A job that decides what a change needs.** A ``changes`` job looks at which paths a pull request touches; packaging, distribution, static
  builds and the like are skipped for a documents-only change. A documents-only pull request went from the full cost to **61 seconds and 1.9 job-minutes**.
- **No incremental builds, and line-table-only debug info, in CI**; network retries on downloads.
- **A cheap optimisation level for a build whose speed does not matter** (a packaging snippet).

Measured warm: a full run **177 and 178 seconds** wall, **15.6 and 15.8 job-minutes**. First runs with a cold cache: 336 to 368 seconds, as expected.

What did not pay, and why it is written down
--------------------------------------------

Rejections are part of the result. Each has a reason, so nobody re-tries it:

``mold`` as the linker
    The default linker (lld) has been the default since Rust 1.90, and the toolchain here is newer.
``nextest`` as the test runner
    A process per test would defeat the in-process lock that makes the tests that spawn programs safe.
``sccache`` for the Arch package build, splitting the real-filesystem job, running the reproducible build in parallel, moving an install check earlier
    None paid in measurement.

A claim that was retracted
--------------------------

A speed-up of the Arch install job was reported from the best of a few runs (365 and 409 seconds before, 270 after). Four releases later the
before-and-after ranges overlapped, so the effect was not demonstrated, and the log says so where the claim was made. After more releases (before:
274, 365, 409; after: 283, 268, 202, 276, 222, 231) it is *supported, not proven*, because the "before" sample is still three. State the number of
samples and say when they overlap.

Release policy: batch, do not release on every merge
----------------------------------------------------

A release per merge cost about **eight minutes of waiting**, four workflows, and a few dozen runner-minutes, and gave users a new patch version every few
minutes for a tool they would update monthly. What it proved beyond what CI already proves on every pull request was only the *publishing* step, and that
changes only when packaging or the release workflows change. It also multiplied the chances of a flaky release job (one failed on a GitHub server error).

The release tool already keeps one release pull request open and updates it with every merge, so batching needs only a policy for *when to merge that
pull request*. A change releases when:

- **10** changes that make a changelog entry are waiting (chores and documents do not count), or
- the oldest waiting change is **7 days** old, or
- the change touches **how releases are published** (the packaging directory, the release workflows), or
- a release was asked for.

Otherwise the shipper says ``release deferred: 3 of 10 changes are waiting`` and finishes. When it does release, it first waits for the workflow that updates the
release pull request, so the batch cannot leave the newest change out.

The policy is a **pure function** with ten tested cases (a few waiting; ten; one short of ten; a week old; just under a week; packaging; a release workflow;
an ordinary workflow; nothing waiting however old; asked for), and the test was shown to fail when the threshold is off by one. After the change an iteration took two tool calls
instead of six.

What it costs: a bigger release when it comes, and a defect found by a release is found later. Both are small because every change passes the whole of CI first, and the
changelog says what is in the release.

Flakes and races
----------------

**Runner flakes.** A job that fails because the runner could not start it, or because GitHub's own server returned an error, is not a failure of the change. The shipper reruns
runner flakes; the one that failed with an HTTP 500 while downloading the release's own assets was rerun by hand once, and the download script now retries five times.

**A rare failure is not disproved by many clean runs.** A test that spawned scripts it had just written failed in CI with *text file busy*; 740 clean local runs on a fast machine had
"shown" it was fine. The fix was by construction: every spawn and every script write behind one lock. A stress test (16 threads, 4 processes burning CPU) failed the original **120 of 120**
runs and the fixed version **0 of 120**. Do not retry the failing step, and do not mark the test flaky: both hide the cause.
