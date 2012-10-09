"""Tests for cement.core.controller."""

from cement.core import exc, controller, handler
from cement.utils import test

class TestController(controller.CementBaseController):
    class Meta:
        label = 'base'
        arguments = [
            (['-f', '--foo'], dict(help='foo option'))
        ]
        usage = 'My Custom Usage TXT'
        
    @controller.expose(hide=True)
    def default(self):
        pass

class TestWithPositionalController(controller.CementBaseController):
    class Meta:
        label = 'base'
        arguments = [
            (['foo'], dict(help='foo option', nargs='?'))
        ]
        
    @controller.expose(hide=True)
    def default(self):
        self.app.render(dict(foo=self.app.pargs.foo))
        
class Embedded(controller.CementBaseController):
    class Meta:
        label = 'embedded_controller'
        stacked_on = 'base'
        stacked_type = 'embedded'
        arguments = [(['-t'], dict())]
        
    @controller.expose(aliases=['emcmd1'], help='This is my help txt')
    def embedded_cmd1(self):
        pass

class Nested(controller.CementBaseController):
    class Meta:
        label = 'nested_controller'
        stacked_on = 'base'
        stacked_type = 'nested'
        arguments = [(['-t'], dict())]
        
    @controller.expose()
    def nested_cmd1(self):
        pass

class DuplicateCommand(controller.CementBaseController):
    class Meta:
        label = 'duplicate_command'
        stacked_on = 'base'
        stacked_type = 'embedded'
        
    @controller.expose()
    def default(self):
        pass
        
class DuplicateAlias(controller.CementBaseController):
    class Meta:
        label = 'duplicate_command'
        stacked_on = 'base'
        stacked_type = 'embedded'
        
    @controller.expose(aliases=['default'])
    def cmd(self):
        pass
        
class Bad(controller.CementBaseController):
    class Meta:
        label = 'bad_controller'
        arguments = []

class BadStackedType(controller.CementBaseController):
    class Meta:
        label = 'bad_stacked_type'
        stacked_on = 'base'
        stacked_type = 'bogus'
        arguments = []
        
class ArgumentConflict(controller.CementBaseController):
    class Meta:
        label = 'embedded'
        stacked_on = 'base'
        stacked_type = 'embedded'
        arguments = [(['-f', '--foo'], dict())]
                
class ControllerTestCase(test.CementTestCase):
    def test_default(self):
        app = self.make_app(base_controller=TestController)
        app.setup()
        app.run()
        
    def test_txt_defined_base_controller(self):
        handler.register(TestController)
        self.app.setup()
    
    @test.raises(exc.InterfaceError)
    def test_invalid_arguments_1(self):
        Bad.Meta.arguments = ['this is invalid']
        handler.register(Bad)

    @test.raises(exc.InterfaceError)
    def test_invalid_arguments_2(self):
        Bad.Meta.arguments = [('this is also invalid', dict())]
        handler.register(Bad)
        
    @test.raises(exc.InterfaceError)
    def test_invalid_arguments_3(self):
        Bad.Meta.arguments = [(['-f'], 'and this is invalid')]
        handler.register(Bad)

    @test.raises(exc.InterfaceError)
    def test_invalid_arguments_4(self):
        Bad.Meta.arguments = 'totally jacked'
        handler.register(Bad)
    
    def test_embedded_controller(self):
        app = self.make_app(argv=['embedded-cmd1'])
        handler.register(TestController)
        handler.register(Embedded)
        app.setup()
        app.run()
        
        check = 'embedded-cmd1' in app.controller._visible_commands
        self.ok(check)

        # also check for the alias here
        check = 'emcmd1' in app.controller._dispatch_map
        self.ok(check)
        
    def test_nested_controller(self):
        app = self.make_app(argv=['nested-controller'])
        handler.register(TestController)
        handler.register(Nested)
        app.setup()
        app.run()
        
        check = 'nested-controller' in app.controller._visible_commands
        self.ok(check)
        
        self.eq(app.controller._dispatch_command['func_name'], '_dispatch')

    @test.raises(exc.FrameworkError)
    def test_bad_stacked_type(self):
        app = self.make_app()
        handler.register(TestController)
        handler.register(BadStackedType)
        app.setup()
        app.run()
        
    @test.raises(exc.FrameworkError)
    def test_duplicate_command(self):
        app = self.make_app()
        handler.register(TestController)
        handler.register(DuplicateCommand)
        app.setup()
        app.run()
    
    @test.raises(exc.FrameworkError)
    def test_duplicate_alias(self):
        app = self.make_app()
        handler.register(TestController)
        handler.register(DuplicateAlias)
        app.setup()
        app.run()
        
    def test_usage_txt(self):
        app = self.make_app()
        handler.register(TestController)
        app.setup()
        self.eq(app.controller._usage_text, 'My Custom Usage TXT')
        
    @test.raises(exc.FrameworkError)
    def test_argument_conflict(self):
        app = self.make_app(base_controller=TestController)
        handler.register(ArgumentConflict)
        app.setup()
        app.run()
    
    def test_default_command_with_positional(self):
        app = self.make_app(base_controller=TestWithPositionalController, 
                            argv=['mypositional'])
        app.setup()
        app.run()
        self.eq(app.get_last_rendered()[0]['foo'], 'mypositional')