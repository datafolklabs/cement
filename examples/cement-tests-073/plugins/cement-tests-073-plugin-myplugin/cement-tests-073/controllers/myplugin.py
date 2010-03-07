"""myplugin controller class to expose commands for cement-tests-073."""

from cement.core.controller import CementController, expose

from cement-tests-073.model.myplugin import mypluginModel

class mypluginController(CementController):
    @expose()              
    def myplugin_command(self, *args, **kw):
        """Register root command that doesn't use a template."""
        myvar = "myplugin root command run() method."
        print myvar
        
        # Even if you're not using a template, return relevant data so that
        # you can still use the --json engine.
        return dict(foo=myvar)
          
    @expose()            
    def myplugin_command_help(self, *args, **kw):
        print "myplugin root command help method."

    @expose('cement-tests-073.templates.myplugin.myplugin_command')              
    def myplugin_command2(self, *args, **kw):
        """Register root command, with Genshi templating."""
        foo = "Hello"
        bar = "World"
        return dict(foo=foo, bar=bar)

    @expose(namespace='myplugin')              
    def myplugin_sub_command(self, *args, **kw):
        """Register sub command for the myplugin namespace."""
        print "myplugin local command method."
        return dict()

