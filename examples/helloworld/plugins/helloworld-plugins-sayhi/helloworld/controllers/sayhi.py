"""sayhi controller class to expose commands for helloworld."""

from cement.core.controller import CementController, expose

from helloworld.model.sayhi import sayhiModel

class sayhiController(CementController):
    @expose()              
    def sayhi_command(self, cli_opts, cli_args):
        """Register root command that doesn't use a template."""
        myvar = "sayhi root command run() method."
        print myvar
        
        # Even if you're not using a template, return relevant data so that
        # you can still use the --json engine.
        return dict(foo=myvar)
          
    @expose()            
    def sayhi_command_help(self, cli_opts, cli_args):
        print "sayhi root command help method."

    @expose('helloworld.templates.sayhi.sayhi_command')              
    def sayhi_command2(self, cli_opts, cli_args):
        """Register root command, with Genshi templating."""
        foo = "Hello"
        bar = "World"
        return dict(foo=foo, bar=bar)

    @expose(namespace='sayhi')              
    def sayhi_sub_command(self, cli_opts, cli_args):
        """Register sub command for the sayhi namespace."""
        print "sayhi local command method."
        return dict()

