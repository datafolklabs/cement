"""Cement core backend module."""

import sys


# global handlers dict
__handlers__ = {}

# global hooks dict
__hooks__ = {}

# Save original stdout/stderr for supressing output.  This is actually reset
# in foundation.CementApp.lay_cement() before nullifying output, but we set
# it here just for a default.
__saved_stdout__ = sys.stdout
__saved_stderr__ = sys.stderr
