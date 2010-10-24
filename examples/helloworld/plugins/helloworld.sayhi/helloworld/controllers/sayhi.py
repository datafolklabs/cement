"""sayhi controller class to expose commands for helloworld."""

from cement.core.controller import CementController, expose

from helloworld.model.sayhi import SayhiModel

class SayhiController(CementController):
    @expose()              
    def sayhi_command(self):
        """Register root command that doesn't use a template."""
        foo = 'bar'
        
        # Even if you're not using a template, return relevant data so that
        # you can still use the --json engine, or similar.
        return dict(foo=foo)
          
    @expose()            
    def sayhi_command_help(self):
        """help methods are accessed as 'command-help'."""
        print "sayhi root command help method."

    @expose('helloworld.templates.sayhi.sayhi_command')              
    def sayhi_command2(self, *args, **kw):
        """Register root command, with Genshi templating."""
        foo = "Hello"
        bar = "World"
        return dict(foo=foo, bar=bar)

    @expose(namespace='sayhi')              
    def sayhi_sub_command(self):
        """Register sub command for the sayhi namespace."""
        foo = 'bar'
        print foo
        return dict(foo=foo)

