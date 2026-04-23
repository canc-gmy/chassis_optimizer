"""Service layer package.

Services are thin orchestrators.  They wire application-layer config and port
interfaces together with domain objects to fulfil use-case logic.

Import rules
------------
- May import from ``chassis_optimizer.app`` and ``chassis_optimizer.domain``.
- Must not import from ``chassis_optimizer.infrastructure`` or ``cli``.
"""

