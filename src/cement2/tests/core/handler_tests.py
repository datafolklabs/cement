"""Tests for cement.core.handler."""

import unittest
from nose.tools import ok_, eq_, raises
from cement2.core import exc, backend, handler, handler, output, meta
from cement2.core import interface
from cement2 import test_helper as _t
from cement2.lib.ext_configparser import ConfigParserConfigHandler

class BogusOutputHandler(meta.MetaMixin):
    class Meta:
        #interface = IBogus
        label = 'bogus_handler'

class BogusOutputHandler2(meta.MetaMixin):
    class Meta:
        interface = output.IOutput
        label = 'bogus_handler'

class BogusHandler3(meta.MetaMixin):
    pass   

class BogusHandler4(meta.MetaMixin):
    class Meta:
        interface = output.IOutput
        # label = 'bogus4'

class DuplicateHandler(output.CementOutputHandler):
    class Meta:
        interface = output.IOutput
        label = 'null'

    def _setup(self, config_obj):
        pass
    
    def render(self, data_dict, template=None):
        pass
        
class BogusInterface1(interface.Interface):
    pass
    
class BogusInterface2(interface.Interface):
    class IMeta:
        pass
    
class TestInterface(interface.Interface):
    class IMeta:
        label = 'test'
        
class TestHandler(meta.MetaMixin):
    class Meta:
        interface = TestInterface
        label = 'test'
        
class HandlerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = _t.prep()
        
    @raises(exc.CementRuntimeError)
    def test_get_invalid_handler(self):
        handler.get('output', 'bogus_handler')

    @raises(exc.CementInterfaceError)
    def test_register_invalid_handler(self):
        handler.register(BogusOutputHandler)

    @raises(exc.CementInterfaceError)
    def test_register_invalid_handler_no_meta(self):
        handler.register(BogusHandler3)

    @raises(exc.CementInterfaceError)
    def test_register_invalid_handler_no_Meta_label(self):
        handler.register(BogusHandler4)
    
    @raises(exc.CementRuntimeError)
    def test_register_duplicate_handler(self):
        from cement2.ext import ext_nulloutput
        handler.register(ext_nulloutput.NullOutputHandler)
        try:
            handler.register(DuplicateHandler)
        except exc.CementRuntimeError:
            raise
    
    @raises(exc.CementInterfaceError)
    def test_register_unproviding_handler(self):
        try:
            handler.register(BogusOutputHandler2)
        except exc.CementInterfaceError:
            del backend.handlers['output']
            raise

    def test_verify_handler(self):
        ok_(handler.registered('output', 'null'))
        eq_(handler.registered('output', 'bogus_handler'), False)
        eq_(handler.registered('bogus_type', 'bogus_handler'), False)

    @raises(exc.CementRuntimeError)
    def test_get_bogus_handler(self):
        handler.get('log', 'bogus')

    @raises(exc.CementRuntimeError)
    def test_get_bogus_handler_type(self):
        handler.get('bogus', 'bogus')

    def test_handler_defined(self):
        for handler_type in ['config', 'log', 'argument', 'plugin', 
                             'extension', 'output', 'controller']:
            yield is_defined, handler_type

        # and check for bogus one too
        eq_(handler.defined('bogus'), False)
    
    def test_handler_list(self):
        self.app.setup()
        handler_list = handler.list('config')
        res = ConfigParserConfigHandler in handler_list
        ok_(res)
    
    @raises(exc.CementRuntimeError)
    def test_handler_list_bogus_type(self):
        self.app.setup()
        handler_list = handler.list('bogus')
    
    def is_defined(handler_type):
        eq_(handler.defined(handler_type), True)

    @raises(exc.CementInterfaceError)
    def test_bogus_interface_no_IMeta(self):
        handler.define(BogusInterface1)

    @raises(exc.CementInterfaceError)
    def test_bogus_interface_no_IMeta_label(self):
        handler.define(BogusInterface2)

    @raises(exc.CementRuntimeError)
    def test_define_duplicate_interface(self):
        handler.define(output.IOutput)
        handler.define(output.IOutput)

    def test_interface_with_no_validator(self):
        handler.define(TestInterface)
        handler.register(TestHandler)
    
    def test_handler_defined(self):
        handler.defined('output')
    
    def test_handler_not_defined(self):
        eq_(handler.defined('bogus'), False)
        
    def test_handler_registered(self):
        eq_(handler.registered('output', 'null'), True)
    
    def test_handler_enabled(self):
        eq_(handler.enabled('output', 'null'), True)
    