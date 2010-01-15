
import re

from cement import namespaces
from cement.core.view import render
    
class CementController(object):
    cli_opts = None
    cli_args = None
    all_commands = []
    hidden_commands = []
      
def expose(template=None, namespace='global', **kwargs):
    """
    Decorator function for plugins to register commands.  Used as:
    
    @expose('app_module.view.template', namespace='namespace')
    def mycommand(self):
        ...
    """
    def decorate(func):
        name = re.sub('_', '-', func.__name__)
        if not namespace in namespaces:
            raise CementRuntimeError, "The namespace '%s' is not defined!" % namespace
        
        func = render(template)(func)        
        
        cmd = {
            'is_hidden' : kwargs.get('is_hidden', False),
            'func' : func
            }
            
        namespaces[namespace].commands[name] = cmd
        return func
    return decorate