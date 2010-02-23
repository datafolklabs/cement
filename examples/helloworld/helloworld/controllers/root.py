"""
This is the RootController for the helloworld application.  This can be used
to expose commands to the root namespace which will be accessible under:

    $ helloworld --help
  
"""

from cement import namespaces
from cement.core.exc import CementArgumentError
from cement.core.controller import CementController, expose
from cement.core.namespace import get_config
from cement.core.log import get_logger

log = get_logger(__name__)
config = get_config()

class RootController(CementController):
    @expose('helloworld.templates.root.error', is_hidden=True)
    def error(self, *args, **kw):
        """
        This can be called when catching exceptions.  It expects an 
        'errors' dictionary to be passed via **kwargs.
        
        """
        if kw.get('errors', None):
            return dict(errors=kw['errors'])
    
    @expose(is_hidden=True)
    def default(self, cli_opts, cli_args):
        """
        This is the default command method.  If no commands are passed to
        helloworld, this one will be executed.  By default it raises an
        exception.
        
        """
        raise CementArgumentError, "A command is required. See --help?"
    
    @expose('helloworld.templates.root.cmd1')
    def cmd1(self, cli_opts, cli_args):
        """This is an example 'root' command.  It should be replaced."""
        foo = 'In helloworld.controllers.root.cmd1()'
        if cli_opts.debug:
            print 'The --debug option was passed'
        
        items = ['one', 'two', 'three']
        return dict(foo=foo, items=items)
    
    @expose()
    def cmd1_help(self, cli_opts, cli_args):
        """This is an example 'root' -help command.  It should be replaced."""
        foo = 'In helloworld.controllers.root.cmd1_help()'
        return dict(foo=foo)
    
    @expose('helloworld.templates.root.get-started')
    def get_started(self, cli_opts, cli_args):
        features = [
            'Multiple Configuration file parsing (default: /etc, ~/)',
            'Command line argument and option parsing',
            'Dual Console/File Logging Support',
            'Full Internal and External (3rd Party) Plugin support',
            'Basic "hook" support',
            'Full MVC support for advanced application design',
            'Text output rendering with Genshi templates',
            'Json output rendering allows other programs to access your CLI-API',
            ]
        
        genshi_link = "http://genshi.edgewall.org/wiki/Documentation/text-templates.html"
        return dict(config=config, features=features, genshi_link=genshi_link)