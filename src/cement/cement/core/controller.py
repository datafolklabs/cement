"""Methods and classes to handle Cement Controller functions."""

from cement import namespaces
from cement.core.log import get_logger
from cement.core.exc import CementRuntimeError
from cement.core.view import render
from cement.core.configuration import set_config_opts_per_cli_opts
    
log = get_logger(__name__)

class CementController(object):
    """Currently just a place holder for more featureful controller."""
    def __init__(self, cli_opts=None, cli_args=None):
        self.cli_opts = cli_opts
        self.cli_args = cli_args
    

def run_controller_command(namespace, func, cli_opts=None, cli_args=None, 
                           *args, **kw):
    """
    Cleanly run a command function from a controller.  Returns a tuple of
    (result_dict, output_txt).
    
    Arguments:
    
        namespace
            The namespace of the controller
        func
            The name of the function
        cli_opts
            Options passed to the command line
        cli_args
            Arguments passed to the command line
        args
            Any additional arguments to pass to the function
        kwargs
            Any additional keyword arguments to pass to the function.
    
    
    Usage:
    
    .. code-block:: python
    
        from cement.core.controller import run_controller_command
        
        run_controller_command('root', 'cmd_name', myarg=True)
        
    """

    # set configurations per what is passed at cli
    for nam in namespaces:
        set_config_opts_per_cli_opts(nam, cli_opts)
        
    controller = namespaces[namespace].controller(cli_opts, cli_args)
    (res, out_txt) = getattr(controller, func)(*args, **kw)
    return (res, out_txt)

class expose(object):
    """
    Decorator function for plugins to expose commands.  Used as:
    
    Arguments:
    
        template
            A template in python module form (i.e 'myapp.templates.mytemplate')
        namespace
            The namespace to expose the command in.  Default: root
    
    
    Optional Keyword Arguments:
    
        is_hidden
            True/False whether command should display on --help.
    
    
    Usage:
    
    .. code-block:: python
    
        class MyController(CementController):
            @expose('myapp.templates.mycontroller.cmd', namespace='root')
            def cmd(self):
                foo="Foo"
                bar="Bar"
                return dict(foo=foo, bar=bar)
                
    """
    def __init__(self, template=None, namespace='root', **kwargs):
        # These get set in __call__
        self.func = None
        self.name = kwargs.get('name', None)
        self.template = template
        self.namespace = namespace
        self.tmpl_module = None
        self.tmpl_file = None
        self.config = namespaces['root'].config
        self.is_hidden = kwargs.get('is_hidden', False)
        self.desc = kwargs.get('desc', None)
        
        if not self.namespace in namespaces:
            raise CementRuntimeError, \
                "The namespace '%s' is not defined!" % self.namespace
                
        # First set output_handler from config
        # DEPRECATION: output_engine
        self.output_handler = None
        if not self.config.has_key('output_handler'):
            if self.config.has_key('output_engine'):
                self.output_handler = self.config['output_engine']
        else:
            self.output_handler = self.config['output_handler']
        
        # The override output_handler from @expose()
        if self.template:
            parts = template.split(':')
            if len(parts) >= 2:
                self.output_handler = parts[0]
                self.template = parts[1]
            elif len(parts) == 1:
                self.template = parts[0]
            else:
                raise CementRuntimeError, "Invalid handler:template identifier."
                        
    def __get__(self, obj, type=None):
        if self.func:
            return self.__class__(self.func.__get__(obj, type))
        else:
            return self.__get__
        
    def __call__(self, func):
        (base, controller, con_namespace) = func.__module__.split('.')
        
        self.func = func
        if not self.name:
            self.name = self.func.__name__
        
        if not self.output_handler:
            log.debug("no output handler configured to generate output " + \
                      "for %s" % self.name)
            
        log.debug("exposing namespaces['%s'].commands['%s'] from '%s'" % \
                 (self.namespace, self.name, self.func.__module__))
                
        # First for the template
        if not self.name:
            self.name = self.func.__name__

        cmd = {
            'is_hidden' : self.is_hidden,
            'original_func' : func,
            'func' : self.name,
            'controller_namespace' : con_namespace,
            }

        # Set the command info in the dest namespace
        namespaces[self.namespace].commands[self.name] = cmd
        self.func = render(self.output_handler, self.template)(self.func)
        return self.func
      
