"""Tests for cement.core.controller."""

from cement.core import exc, controller, handler
from cement.utils import test

class BogusController(controller.CementBaseController):
    class Meta:
        interface = controller.IController
        label = None
  
class BogusController2(controller.CementBaseController):
    class Meta:
        interface = controller.IController
        label = 'bogus2'
        description = 'Bogus Base Controller2'
        config_defaults = {}
        arguments = ['bad']
        hide = False
        stacked_on = 'base'

class BogusController3(controller.CementBaseController):
    class Meta:
        interface = controller.IController
        label = 'bogus3'
        description = 'Bogus Base Controller3'
        config_defaults = {}
        arguments = [(['--ok'], 'bad')]
        hide = False
        stacked_on = 'base'

class BogusController4(controller.CementBaseController):
    class Meta:
        interface = controller.IController
        label = 'bogus4'
        description = 'Bogus Base Controller4'
        config_defaults = {}
        arguments = [('bad', dict())]
        hide = False
        stacked_on = 'base'
          
class TestBaseController(controller.CementBaseController):
    class Meta:
        interface = controller.IController
        label = 'base'
        description = 'Test Base Controller'
        config_section = 'base'
        config_defaults = dict(test_base_default=1)
        arguments = []
        hide = False
    
    @controller.expose()
    def default(self):
        print('Default')
        
    @controller.expose(aliases=['mycmd'])
    def my_command(self):
        print('My Command')
     
class TestBaseController2(controller.CementBaseController):
    class Meta:
        interface = controller.IController
        label = 'base'
        description = 'Test Base Controller2'
        config_defaults = {}
        arguments = []
        hide = False
        epilog = 'Test Epilog'
        usage = 'Test Usage'
        
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
        config_section = 'base'
        config_defaults = dict(test_stacked_default=2)

        arguments = [
            (['--foo-stacked'], dict(action='store'))
            ]
            
        stacked_on = 'base'
        hide = False
    
    @controller.expose(aliases=['my-stckd-cmd'], help='my stacked command')
    def my_stacked_command(self):
        pass

class DoubleStackedController(controller.CementBaseController):
    class Meta:
        interface = controller.IController
        label = 'double_stacked'
        description = 'Double Stacked Controller'
        config_defaults = None
        defaults = dict(foo='bar') # covers deprecated code
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
        config_defaults = dict(test_secondary_default=3)
        aliases = ['sec']
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
        
        config_defaults = dict(
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
        
        config_defaults = dict(
            foo='bar',
            )

        arguments = [
            (['-f2', '--foo2'], dict(action='store'))
            ]
    
    @controller.expose(hide=True, aliases=['my_command'])
    def mycmd(self):
        pass

class TestDuplicate3Controller(controller.CementBaseController):
    class Meta:
        interface = controller.IController
        label = 'test_duplicate3'
        description = 'Test Duplicate3 Controller'
        stacked_on = 'base'
        
        config_defaults = dict(
            foo='bar',
            )

        arguments = [
            (['-f2', '--foo2'], dict(action='store'))
            ]
    
    @controller.expose(hide=True, aliases=['mycmd'])
    def dup3(self):
        pass
        
class SameNameController(controller.CementBaseController):
    class Meta:
        interface = controller.IController
        label = 'same_name'
        description = 'Same Name Controller'
        config_defaults = dict()
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
        config_defaults = dict()
        arguments = []
        stacked_on = 'base'
    
    @controller.expose(aliases=['test_secondary'])
    def test_command(self):
        pass
        
class ControllerTestCase(test.CementTestCase):
    def setUp(self):
        self.app = self.make_app(
            argv=['my-command'], 
            base_controller=TestBaseController
            )
        
    @test.raises(exc.InterfaceError)
    def test_invalid_controller(self):
        handler.register(BogusController)

    @test.raises(exc.InterfaceError)
    def test_invalid_arguments_tuple(self):
        handler.register(BogusController2)
        self.app.setup()
        self.app.run()

    @test.raises(exc.InterfaceError)
    def test_invalid_arguments_dict(self):
        handler.register(BogusController3)
        self.app.setup()
        self.app.run()    

    @test.raises(exc.InterfaceError)
    def test_invalid_arguments_list(self):
        handler.register(BogusController4)
        self.app.setup()
        self.app.run()

    def test_base_controller(self):
        self.app.setup()
        self.app.run()

    def test_base_controller_by_name(self):
        self.app = self.make_app(
            argv=['my-command'], 
            base_controller=None
            )
        handler.register(TestBaseController)
        self.app.setup()
        
    def test_stacked_controller(self):
        app = self.make_app(
            argv=['my-stacked-command',], 
            base_controller=TestBaseController,
            )
        handler.register(TestStackedController)
        handler.register(DoubleStackedController)
        app.setup()
        app.run()

    def test_secondary_controller(self):
        app = self.make_app(
            argv=['test_secondary', 'my-secondary-command'], 
            base_controller=TestBaseController,
            )
        handler.register(TestSecondaryController)
        app.setup()
        app.controller._setup(app)
        app.run()

    def test_controller_alias(self):
        app = self.make_app(
            argv=['sec', 'my-secondary-command'], 
            base_controller=TestBaseController,
            )
        handler.register(TestSecondaryController)
        app.setup()
        app.controller._setup(app)
        app.run()
        self.eq(app.controller._meta.label, 'test_secondary')
        
    @test.raises(SystemExit)
    def test_bad_command(self):
        app = self.make_app(argv=['bogus-command'])
        app.setup()
        app.run()

    def test_default_command(self):
        app = self.make_app(argv=[], base_controller=TestBaseController)
        app.setup()
        app.run()

    def test_command_alias(self):
        app = self.make_app(argv=['mycmd'], base_controller=TestBaseController)
        app.setup()
        app.run()
   
    def test_stacked_command(self):
        app = self.make_app(
            argv=['my-command'], 
            base_controller=TestBaseController
            )
        app.setup()
        app.run()
     
    @test.raises(exc.FrameworkError)
    def test_duplicate_command(self):
        handler.register(TestDuplicateController)
        self.app.setup()
    
        try:
            self.app.run()
        except exc.FrameworkError as e:
            self.ok(e.msg.find('duplicate'))
            raise

    @test.raises(exc.FrameworkError)
    def test_duplicate_hidden_command(self):
        handler.register(TestDuplicate2Controller)
        self.app.setup()
    
        try:
            self.app.run()
        except exc.FrameworkError:
            # FIX ME: Check the error message is right error
            raise

    @test.raises(SystemExit)
    def test_bad_command(self):
        self.app = self.make_app(
            argv=['bogus-command'], 
            base_controller=TestBaseController
            )
        self.app.setup()
    
        try:
            self.app.run()
        except SystemExit:
            raise

    def test_bad_command2(self):
        self.app = self.make_app(
            argv=[], 
            base_controller=TestBaseController
            )
        self.app.setup()
        self.app.controller.command = None
        
        try:
            self.app.run()
        except SystemExit:
            raise

    def test_controller_defaults(self):
        self.app = self.make_app(
            argv=['my-command'], 
            base_controller=TestBaseController,
            )
        handler.register(TestStackedController)
        self.app.setup()
        self.app.run()
        self.eq(self.app.config.get('base', 'test_base_default'), 1)
        self.eq(self.app.config.get('base', 'test_stacked_default'), 2)
    
    @test.raises(exc.FrameworkError)
    def test_same_name_controller(self):
        handler.register(SameNameController)
        self.app.setup()
    
    @test.raises(exc.FrameworkError)
    def test_same_name_alias_controller(self):
        handler.register(TestSecondaryController)
        handler.register(SameNameAliasController)
        self.app.setup()
        self.app.run()
    
    @test.raises(exc.FrameworkError)
    def test_duplicate_alias(self):
        handler.register(TestSecondaryController)
        handler.register(TestDuplicate3Controller)
        self.app.setup()
        try:
            self.app.run()
        except exc.FrameworkError as e:
            self.ok(e.msg.find('collides'))
            raise

    def test_usage_text(self):
        self.app.setup()
        contr = TestBaseController2()
        contr._setup(self.app)
        self.eq(contr._usage_text, 'Test Usage')
    