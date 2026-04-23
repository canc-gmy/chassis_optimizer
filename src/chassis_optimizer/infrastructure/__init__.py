"""Infrastructure adapters package.

Infrastructure modules implement application-layer ports (Protocols) and
handle all I/O: file reading, database access, and external solver calls.

Import rules
------------
- May import from ``chassis_optimizer.app`` (to implement ports) and
  ``chassis_optimizer.domain``.
- Must not import from ``chassis_optimizer.services`` or ``cli``.
"""

