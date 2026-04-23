"""Module entry point for ``python -m chassis_optimizer``.

Running the package as a module delegates directly to
:func:`chassis_optimizer.cli.main.run`, which parses ``sys.argv`` and
returns an integer exit code.

Usage::

    python -m chassis_optimizer [<command>] [<options>]

Exit codes
----------
0
    Success.
1
    User-visible error (bad config path, validation failure, etc.).
"""

from chassis_optimizer.cli.main import run


if __name__ == "__main__":
    raise SystemExit(run())
