
from pytest import raises
from cement.core.exc import FrameworkError, InterfaceError, CaughtSignal

class TestExceptions(object):
    def test_frameworkerror(self):
        with raises(FrameworkError, match=".*framework exception.*") as e:
            raise FrameworkError("test framework exception message")

    def test_interfaceerror(self):
        with raises(InterfaceError, match=".*interface exception.*") as e:
            raise InterfaceError("test interface exception message")

    def test_caughtsignal(self):
        with raises(CaughtSignal, match=".*Caught signal.*") as e:
            raise CaughtSignal(1, 2)
        assert e.value.signum == 1
        assert e.value.frame == 2
