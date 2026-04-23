"""Top-level package for chassis_optimizer.

Public API
----------
__version__ : str
    The package version string following PEP 440 (MAJOR.MINOR.PATCH).

Import rules
------------
This package ``__init__`` must remain import-side-effect free.  It may only
expose the version string and re-export symbols that are part of the stable
public API.  Do not import heavy dependencies at module level here.
"""

__all__ = ["__version__"]
__version__ = "0.1.0"
