"""Tests for cement.core.exc."""

import unittest
from nose.tools import eq_, raises
from nose import SkipTest
from cement2.core import exc
from cement2 import test_helper as _t

class ExceptionTestCase(unittest.TestCase):
    def setUp(self):
        self.app = _t.prep()

    @raises(exc.CementConfigError)    
    def test_cement_config_error(self):
        try:
            raise exc.CementConfigError("CementConfigError Test")
        except exc.CementConfigError as e:
            eq_(e.msg, "CementConfigError Test")
            eq_(e.__str__(), "CementConfigError Test")
            raise
        
    @raises(exc.CementRuntimeError)
    def test_cement_runtime_error(self):
        try:
            raise exc.CementRuntimeError("CementRuntimeError Test")
        except exc.CementRuntimeError as e:
            eq_(e.msg, "CementRuntimeError Test")
            eq_(e.__str__(), "CementRuntimeError Test")
            raise
        
    @raises(exc.CementArgumentError)
    def test_cement_argument_error(self):
        try:
            raise exc.CementArgumentError("CementArgumentError Test")
        except exc.CementArgumentError as e:
            eq_(e.msg, "CementArgumentError Test")
            eq_(e.__str__(), "CementArgumentError Test")
            raise

    @raises(exc.CementInterfaceError)
    def test_cement_interface_error(self):
        try:
            raise exc.CementInterfaceError("CementInterfaceError Test")
        except exc.CementInterfaceError as e:
            eq_(e.msg, "CementInterfaceError Test")
            eq_(e.__str__(), "CementInterfaceError Test")
            raise

    @raises(exc.CementSignalError)
    def test_cement_signal_error(self):
        try:
            import signal
            raise exc.CementSignalError(signal.SIGTERM, 5)
        except exc.CementSignalError as e:
            eq_(e.signum, signal.SIGTERM)
            eq_(e.frame, 5)
            raise