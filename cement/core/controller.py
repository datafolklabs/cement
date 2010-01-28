"""Methods and classes to handle Cement Controller functions."""
import re
from pkgutil import get_data
from genshi.template import NewTextTemplate

from cement import namespaces, SAVED_STDOUT, SAVED_STDERR, \
                   buf_stdout, buf_stderr
from cement.core.log import get_logger
from cement.core.exc import CementRuntimeError
from cement.core.view import render

    
log = get_logger(__name__)

class CementController(object):
    """Currently just a place holder for more featureful controller."""
    def __init__(self):
        pass

def run_controller_command(namespace, func, *args, **kwargs):
    """
    Cleanly run a command function from a controller.
    
    Arguments:
    
        namespace
            The namespace of the controller
        func
            The name of the function
        args
            Any additional arguments to pass to the function
        kwargs
            Any additional keyword arguments to pass to the function.
    
    
    Usage:
    
    .. code-block:: python
    
        from cement.core.controller import run_controller_command
        
        run_controller_command('root', 'cmd_name', myarg=True)
        
    """
    controller = namespaces[namespace].controller()
    func = getattr(controller, func)(*args, **kwargs)
                      
        
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
        
        if self.template:
            # Mock up the template path
            parts = template.split('.')
            self.tmpl_file = "%s.txt" % parts.pop() # the last item is the file            
            self.tmpl_module = '.'.join(parts) # left over in at the beginning
        
        if not self.namespace in namespaces:
            raise CementRuntimeError, \
                "The namespace '%s' is not defined!" % self.namespace
                        
    def __get__(self, obj, type=None):
        if self.func:
            return self.__class__(self.func.__get__(obj, type))
        else:
            return self.__get__
        
    def __call__(self, func):
        (base, controller, con_namespace) = func.__module__.split('.')
        self.func = func
        self.json_func = func
        
        log.debug("exposing namespaces['%s'].commands['%s'] from '%s'" % \
                 (self.namespace, self.func.__name__, self.func.__module__))
                
        # First for the template
        if not self.name:
            self.name = self.func.__name__
        cmd_name = re.sub('_', '-', self.name)
        cmd = {
            'is_hidden' : self.is_hidden,
            'original_func' : func,
            'func' : self.name,
            'controller_namespace' : con_namespace,
            }

        # Set the command info in the dest namespace
        namespaces[self.namespace].commands[cmd_name] = cmd
        self.func = render(self.template)(self.func)
        return self.func
      