"""CLI package for chassis_optimizer.

This package contains all command-line interface code.  Its only external
dependency within the project is the ``app`` and ``services`` layers.

Import rules
------------
- May import from ``chassis_optimizer.app``, ``chassis_optimizer.services``,
  and ``chassis_optimizer.infrastructure`` (for adapter wiring at startup).
- Must not be imported by any other project layer.
"""

