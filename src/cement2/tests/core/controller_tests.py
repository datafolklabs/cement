"""Tests for cement.core.controller."""

import sys
from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement2.core import exc, controller, handler
from cement2 import test_helper as _t

class BogusController(controller.CementBaseController):
    class meta:
        interface = controller.IController
        label = 'bogus'

class TestBaseController(controller.CementBaseController):
    class meta:
        interface = controller.IController
        label = 'base'
        description = 'Test Base Controller'
        defaults = {}
        arguments = []
        hide = False
    
    @controller.expose(aliases=['mycmd'])
    def my_command(self):
        pass
        
class TestStackedController(controller.CementBaseController):
    class meta:
        interface = controller.IController
        label = 'test_stacked'
        description = 'Test Stacked Controller'
        defaults = dict(
            foo='bar',
            )

        arguments = [
            (['-f', '--foo'], dict(action='store'))
            ]
            
        stacked_on = 'base'
        hide = False
    
    @controller.expose(aliases=['mycmd'])
    def my_stacked_command(self):
        pass

class TestSecondaryController(controller.CementBaseController):
    class meta:
        interface = controller.IController
        label = 'test_secondary'
        description = 'Test Secondary Controller'
        defaults = dict(
            foo='bar',
            )

        arguments = [
            (['-f2', '--foo2'], dict(action='store'))
            ]
    
    @controller.expose()
    def my_secondary_command(self):
        pass

class TestDuplicateController(controller.CementBaseController):
    class meta:
        interface = controller.IController
        label = 'test_duplicate'
        description = 'Test Duplicate Controller'
        stacked_on = 'base'
        
        defaults = dict(
            foo='bar',
            )

        arguments = [
            (['-f2', '--foo2'], dict(action='store'))
            ]
    
    @controller.expose()
    def my_command(self):
        pass
         
class TestDuplicate2Controller(controller.CementBaseController):
    class meta:
        interface = controller.IController
        label = 'test_duplicate2'
        description = 'Test Duplicate2 Controller'
        stacked_on = 'base'
        
        defaults = dict(
            foo='bar',
            )

        arguments = [
            (['-f2', '--foo2'], dict(action='store'))
            ]
    
    @controller.expose(hide=True)
    def my_command(self):
        pass
        
@raises(exc.CementInterfaceError)
def test_invalid_controller():
    _t.prep()
    handler.register(BogusController)

def test_base_controller():
    app = _t.prep()
    app.argv = ['my-command']
    handler.register(TestBaseController)
    app.controller = TestBaseController()
    app.setup()
    app.run()

def test_stacked_controller():
    app = _t.prep()
    app.argv = ['my-command']
    handler.register(TestBaseController)
    handler.register(TestStackedController)
    app.controller = TestBaseController()
    app.setup()
    app.run()

def test_secondary_controller():
    app = _t.prep()
    app.argv = ['my-command']
    handler.register(TestBaseController)
    handler.register(TestSecondaryController)
    app.controller = TestBaseController()
    app.setup()
    app.run()

@raises(SystemExit)
def test_bad_command():
    app = _t.prep()
    app.argv = ['bogus-command']
    handler.register(TestBaseController)
    app.controller = TestBaseController()
    app.setup()

    try:
        app.run()
    except SystemExit:
        raise

@raises(NotImplementedError) 
def test_default_command():
    app = _t.prep()
    app.argv = ['default']
    handler.register(TestBaseController)
    app.controller = TestBaseController()
    app.setup()
    app.run()
    
    try:
        app.run()
    except NotImplementedError:
        raise
       
def test_command_alias():
    app = _t.prep()
    app.argv = ['mycmd']
    handler.register(TestBaseController)
    app.controller = TestBaseController()
    app.setup()
    app.run()
   
def test_stacked_command():
    app = _t.prep()
    app.argv = ['my-stacked-command']
    handler.register(TestBaseController)
    handler.register(TestStackedController)
    app.controller = TestBaseController()
    app.setup()
    app.run()
     
@raises(exc.CementRuntimeError)
def test_duplicate_command():
    app = _t.prep()
    app.argv = ['my-command']
    handler.register(TestBaseController)
    handler.register(TestDuplicateController)
    app.controller = TestBaseController()
    app.setup()
    
    try:
        app.run()
    except exc.CementRuntimeError:
        raise

@raises(exc.CementRuntimeError)
def test_duplicate_hidden_command():
    app = _t.prep()
    app.argv = ['my-command']
    handler.register(TestBaseController)
    handler.register(TestDuplicate2Controller)
    app.controller = TestBaseController()
    app.setup()
    
    try:
        app.run()
    except exc.CementRuntimeError:
        raise
    
def test_bogus_dispatch():
    app = _t.prep()
    app.argv = ['default']
    handler.register(TestBaseController)
    app.controller = TestBaseController()
    app.setup()
    
    # no command
    app.controller.command = None
    app.controller.dispatch()
    
    # bad command
    app.controller.command = 'bogus-command'
    app.controller.dispatch()
