"""Tests for cement.core.controller."""

from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement2.core import exc, controller, handler
from cement2 import test_helper as _t
_t.prep()

class BogusController(controller.CementBaseController):
    class Meta:
        interface = controller.IController
        label = None
  
class BogusController2(controller.CementBaseController):
    class Meta:
        interface = controller.IController
        label = 'bogus2'
        description = 'Bogus Base Controller2'
        defaults = {}
        arguments = ['bad']
        hide = False
        stacked_on = 'base'

class BogusController3(controller.CementBaseController):
    class Meta:
        interface = controller.IController
        label = 'bogus3'
        description = 'Bogus Base Controller3'
        defaults = {}
        arguments = [(['--ok'], 'bad')]
        hide = False
        stacked_on = 'base'

class BogusController4(controller.CementBaseController):
    class Meta:
        interface = controller.IController
        label = 'bogus4'
        description = 'Bogus Base Controller4'
        defaults = {}
        arguments = [('bad', dict())]
        hide = False
        stacked_on = 'base'
          
class TestBaseController(controller.CementBaseController):
    class Meta:
        interface = controller.IController
        label = 'base'
        description = 'Test Base Controller'
        defaults = dict(test_base_default=1)
        arguments = []
        hide = False
    
    @controller.expose(aliases=['mycmd'])
    def my_command(self):
        pass
     
class TestBaseController2(controller.CementBaseController):
    class Meta:
        interface = controller.IController
        label = 'base'
        description = 'Test Base Controller2'
        defaults = {}
        arguments = []
        hide = False
    
    @controller.expose()
    def my_command(self):
        pass
           
    @controller.expose()
    def my_command(self):
        pass
        
class TestStackedController(controller.CementBaseController):
    class Meta:
        interface = controller.IController
        label = 'test_stacked'
        description = 'Test Stacked Controller'
        defaults = dict(test_stacked_default=2)

        arguments = [
            (['--foo-stacked'], dict(action='store'))
            ]
            
        stacked_on = 'base'
        hide = False
    
    @controller.expose(aliases=['mycmd'])
    def my_stacked_command(self):
        pass

class DoubleStackedController(controller.CementBaseController):
    class Meta:
        interface = controller.IController
        label = 'double_stacked'
        description = 'Double Stacked Controller'
        defaults = dict()
        arguments = []
        stacked_on = 'test_stacked'
    
    @controller.expose()
    def double_stacked_command(self):
        pass
        
class TestSecondaryController(controller.CementBaseController):
    class Meta:
        interface = controller.IController
        label = 'test_secondary'
        description = 'Test Secondary Controller'
        defaults = dict(test_secondary_default=3)

        arguments = [
            (['-f2', '--foo2'], dict(action='store'))
            ]
    
    @controller.expose()
    def my_secondary_command(self):
        pass

class TestDuplicateController(controller.CementBaseController):
    class Meta:
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
    class Meta:
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
    
    @controller.expose(hide=True, aliases=['my_command'])
    def mycmd(self):
        pass

class SameNameController(controller.CementBaseController):
    class Meta:
        interface = controller.IController
        label = 'same_name'
        description = 'Same Name Controller'
        defaults = dict()
        arguments = []
        stacked_on = 'base'
        
    @controller.expose()
    def same_name(self):
        pass

class SameNameAliasController(controller.CementBaseController):
    class Meta:
        interface = controller.IController
        label = 'same_name_alias'
        description = 'Same Name Alias Controller'
        defaults = dict()
        arguments = []
        stacked_on = 'base'
    
    @controller.expose(aliases=['test_secondary'])
    def test_command(self):
        pass
        
@raises(exc.CementInterfaceError)
def test_invalid_controller():
    _t.prep()
    handler.register(BogusController)

@raises(exc.CementInterfaceError)
def test_invalid_arguments_tuple():
    _t.prep()
    app = _t.prep()
    app.argv = ['my-command']
    handler.register(TestBaseController)
    app.controller = TestBaseController()
    handler.register(BogusController2)
    app.setup()
    app.run()

@raises(exc.CementInterfaceError)
def test_invalid_arguments_dict():
    _t.prep()
    app = _t.prep()
    app.argv = ['my-command']
    handler.register(TestBaseController)
    app.controller = TestBaseController()
    handler.register(BogusController3)
    app.setup()
    app.run()    

@raises(exc.CementInterfaceError)
def test_invalid_arguments_list():
    _t.prep()
    app = _t.prep()
    app.argv = ['my-command']
    handler.register(TestBaseController)
    app.controller = TestBaseController()
    handler.register(BogusController4)
    app.setup()
    app.run()

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
    handler.register(DoubleStackedController)
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
def test_duplicate_alias():
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

def test_bad_command2():
    app = _t.prep()
    app.argv = []
    handler.register(TestBaseController)
    app.controller = TestBaseController()
    app.controller.command = None
    app.setup()
    
    try:
        app.run()
    except SystemExit:
        raise

def test_controller_defaults():
    app = _t.prep()
    
    app.controller = TestBaseController()
    handler.register(TestBaseController)
    handler.register(TestStackedController)
    handler.register(TestSecondaryController)
    app.setup()
    
    eq_(app.config.get('base', 'test_base_default'), 1)
    eq_(app.config.get('base', 'test_stacked_default'), 2)
    eq_(app.config.get('test_secondary', 'test_secondary_default'), 3)
    
@raises(exc.CementRuntimeError)
def test_same_name_controller():
    app = _t.prep()
    app.argv = ['my-command']
    app.controller = TestBaseController()
    handler.register(TestBaseController)
    handler.register(SameNameController)
    app.setup()
    
@raises(exc.CementRuntimeError)
def test_same_name_alias_controller():
    app = _t.prep()
    app.argv = ['my-command']
    app.controller = TestBaseController()
    handler.register(TestBaseController)
    handler.register(TestSecondaryController)
    handler.register(SameNameAliasController)
    app.setup()
    app.run()