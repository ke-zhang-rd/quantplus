"""
setup.py for quantplus.

Almost all metadata (name, version scheme, dependencies) lives in
pyproject.toml, per modern (PEP 621) setuptools convention. This file
exists only because compiling a Cython + C++ extension still needs an
imperative `ext_modules=cythonize(...)` call -- that part can't be
expressed declaratively in pyproject.toml alone.
"""

from setuptools import setup, Extension

try:
    from Cython.Build import cythonize
except ImportError as exc:
    raise ImportError(
        "Cython is required to build this package. Install it first:\n"
        "    pip install Cython\n"
        "then re-run `pip install -e .`"
    ) from exc

extensions = [
    Extension(
        name="quantplus._crr_pricer",
        sources=[
            "quantplus/_crr_pricer.pyx",
            "quantplus/csrc/crr_core.cpp",
        ],
        include_dirs=["quantplus/csrc"],
        language="c++",
        extra_compile_args=["-O2", "-std=c++17"],
    )
]

setup(
    ext_modules=cythonize(
        extensions,
        compiler_directives={"language_level": "3", "linetrace": False},
    ),
)
