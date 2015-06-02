"""Cement core backend module."""

# Note: Nothing is covered here because this file is imported before nose and
# coverage take over.. and so its a false positive that nothing is covered.

import sys  # pragma: nocover

VERSION = (2, 7, 1, 'alpha', 0)  # pragma: nocover

# Save original stdout/stderr for supressing output.  This is actually reset
# in foundation.CementApp.lay_cement() before nullifying output, but we set
# it here just for a default.
__saved_stdout__ = sys.stdout  # pragma: nocover
__saved_stderr__ = sys.stderr  # pragma: nocover
