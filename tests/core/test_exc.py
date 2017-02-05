"""Tests for cement.core.exc."""

from cement.core import exc
from cement.utils import test


class ExceptionTestCase(test.CementCoreTestCase):

    @test.raises(exc.FrameworkError)
    def test_cement_runtime_error(self):
        try:
            raise exc.FrameworkError("FrameworkError Test")
        except exc.FrameworkError as e:
            self.eq(e.msg, "FrameworkError Test")
            self.eq(e.__str__(), "FrameworkError Test")
            raise

    @test.raises(exc.InterfaceError)
    def test_cement_interface_error(self):
        try:
            raise exc.InterfaceError("InterfaceError Test")
        except exc.InterfaceError as e:
            self.eq(e.msg, "InterfaceError Test")
            self.eq(e.__str__(), "InterfaceError Test")
            raise

    @test.raises(exc.CaughtSignal)
    def test_cement_signal_error(self):
        try:
            import signal
            raise exc.CaughtSignal(signal.SIGTERM, 5)
        except exc.CaughtSignal as e:
            self.eq(e.signum, signal.SIGTERM)
            self.eq(e.frame, 5)
            raise
