"""This is the Example controller for helloworld."""

from cement import namespaces
from cement.core.log import get_logger
from cement.core.controller import CementController, expose
from cement.core.hook import run_hooks

from helloworld.model.example import ExampleModel

log = get_logger(__name__)

class ExampleController(CementController):
    @expose(namespace='root') # no template, root namespace (default)
    def ex1(self, cli_opts, cli_args):
        """
        This is how to add a local/plugin subcommand because it will be  
        under the 'example' namespace.  You would access this subcommand as:
    
            $ myapp example ex1
        
        """

        # Note, the 'print' statement should not be used, rather use the
        # log or return data to the template.
        
        # Commands are all passed the cli_opts, cli_args from the command line.
        
        # Here we show how to run a hook that we've defined in
        # helloworld.plugins.example:
        for res in run_hooks('my_example_hook'):
            print res
        
        # This command has no template, but if we return something we
        # can still access the json output via --json.
        return dict(foo='bar')
        
    @expose(namespace='root')
    def ex1_help(self, cli_opts, cli_args):
        """Using the print statement is ok for help methods."""
        print "This is the help method for ex1."
    
    @expose('helloworld.templates.example.ex2', namespace='example')    
    def ex2(self, cli_opts, cli_args): 
        """
        This is an example root command.  See --help.  When commands are
        called, they are passed the cli options and cli_args passed after it.
        
        Notice that you can specify the namespace via the decorator parameters.
        If a plugin has any non-root commands they are grouped under a 
        single command to the base cli application.  For example, you will 
        see root commands and namespaces* when you execute:
        
            myapp --help
            
            
        If 'myplugin' has local commands, you will see 'myplugin*' show up in 
        the root commands list, and then the plugin subcommands will be seen 
        under:
        
            myapp myplugin --help
            
        
        This is done to give different options in how your application works.
        """
        
        # Here we are using our Example model, and then returning a dictionary
        # to our @expose() decorator where it will be rendered with Genshi.
        example = ExampleModel()
        example.label = 'This is my Example Model'

        # You can see if options where passed.  These are set in 
        # myapp/plugins/example.py:
        if cli_opts.root_option:
            # --root-option was passed, do something
            log.info('%s passed by --root-option' % cli_opts.root_option)

        return dict(foo=True, example=example, items=['one', 'two', 'three'])

#    @expose(namespace='other_plugin')
#    def ex3(self, cli_opts, cli_args):
#        """
#        This is how to add a local/plugin subcommand to another namespace.  It
#        is possible to use this in conjunction with the options_hook() to add 
#        additional functionality to a completely other namespace:
#    
#            $ myapp other_plugin ex3
#        
#        """
#        log.info("In helloworld_core namespace")
#        return dict(foo='bar')