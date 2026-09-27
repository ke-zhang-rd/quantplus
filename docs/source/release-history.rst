===============
Release History
===============

Initial release (2026-09-28)
---------------------------

This first documented release of ``quantplus`` introduces the package as a small,
performance-oriented option-pricing library built around the Cox-Ross-Rubinstein
(CRR) binomial model.

Included features
~~~~~~~~~~~~~~~~~

- CRR option pricing for European and American options
- Black-Scholes closed-form pricing for benchmarking
- tree-output utilities for inspecting terminal stock and option states
- Cython-based Python bindings around a native C++ implementation
- regression tests covering correctness and convergence behavior

Project goals
~~~~~~~~~~~~~

The package is intentionally focused on a narrow but important problem: pricing
vanilla options with transparent numerical methods and a simple API. The design is
meant to be easy for users to understand while still leveraging native code for
performance-critical computations.

Future direction
~~~~~~~~~~~~~~~~

The project can reasonably expand in several directions, including:

- more option types and payoff structures
- more advanced Greeks calculations
- additional numerical benchmarks and validation examples
- more documentation and usage examples for quantitative finance workflows

The current release is deliberately small and readable, making it a solid base for
future extension without increasing conceptual complexity.
