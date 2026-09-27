===================================
Minimum Version Policy
===================================

This project follows the standard scientific-Python policy for supported runtime
versions. In practical terms, this means the minimum supported version is chosen
carefully to balance compatibility, user convenience, and the cost of supporting
older interpreters.

Python support policy
---------------------

The package is intended to support a modern Python baseline while remaining easy
to install across common development environments. The general principle is:

- the project supports at least the minor versions of Python released within a
  recent support window
- it keeps pace with the latest supported minor releases
- the minimum version is set explicitly in the packaging metadata

For this project, the current packaging metadata declares Python 3.9+ in
``pyproject.toml``. That means the library is designed to work with recent Python
versions while avoiding unnecessary restrictions on users who maintain modern
environments.

NumPy policy
------------

The package does not currently depend on NumPy directly, but the broader scientific
Python ecosystem often uses the same versioning model. A policy aligned with
`NEP 29 <https://numpy.org/neps/nep-0029-deprecation_policy.html>`__ is a good fit
for projects that want to remain broadly compatible while still adopting new
runtime features when they become stable.

In other words:

- support is kept to recent Python and NumPy releases
- minimum versions are adjusted at appropriate release boundaries
- patch releases avoid unnecessary compatibility breakage

This helps keep the package usable across development environments without
committing to a long, costly deprecation burden.

Why this matters for this project
---------------------------------

Because ``quantplus`` includes compiled Cython/C++ code, the build environment is
more sensitive to runtime and compiler changes than pure-Python libraries. A clear
minimum-version policy ensures that:

- users know the supported baseline
- CI systems can be configured reliably
- build tooling remains stable across releases
- compiled extensions continue to work across supported environments

The project is therefore expected to modernize its minimum supported versions at
feature releases rather than patch releases, unless a critical compatibility fix
requires otherwise.
