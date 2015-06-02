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


# Backwards compatibility
from ..utils.misc import _inspect_app


# Users applications shouldn't use __hooks__ and __handlers__ directly,
# as this was an implementation detail. However, some tests rely on them,
# that's why we fake their behavior.

class _FakeHooks(object):

    def __contains__(self, name):
        app = _inspect_app(sys._getframe(1))
        return name in app.hooks

    def __getitem__(self, name):
        app = _inspect_app(sys._getframe(1))
        return app.hooks._hooks[name]


class _FakeHandlers(object):

    def __getitem__(self, name):
        app = _inspect_app(sys._getframe(1))
        return app.handlers._handlers[name]

    def __delitem__(self, name):
        app = _inspect_app(sys._getframe(1))
        del app.handlers._handlers[name]


__hooks__ = _FakeHooks()
__handlers__ = _FakeHandlers()
