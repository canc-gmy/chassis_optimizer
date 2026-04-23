"""Application layer package.

The ``app`` layer owns typed configuration models and port interfaces
(Protocols).  It acts as the contract boundary between the domain and
infrastructure layers.

Import rules
------------
- May import from ``chassis_optimizer.domain`` only.
- Must not import from ``infrastructure``, ``services``, or ``cli``.
"""

