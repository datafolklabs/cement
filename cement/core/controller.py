"""Methods and classes to handle Cement Controller functions."""
import re

from cement import namespaces
from cement.core.log import get_logger
from cement.core.exc import CementRuntimeError
from cement.core.view import render
    
log = get_logger(__name__)

class CementController(object):
    """Currently just a place holder for more featureful controller."""
    pass
      
def expose(template=None, namespace='global', **kwargs):
    """
    Decorator function for plugins to expose commands.  Used as:
    
    Arguments:
    
        template -- A template in python module form 
                    (i.e 'myapp.templates.mytemplate')
        
        namespace -- The namespace to expose the command in.  Default: global
        
        kwargs -- Options kwargs.
        
    Usage: 
    
        @expose('app_module.view.template', namespace='namespace')
        def mycommand(self):
            ...
    
    Option Keyword Arguments:
    
        is_hidden -- True/False whether command should display on --help.
        
    """
    def decorate(func):
        """
        Decorate the function and expose it to the namespace's commands
        dict.
        """
        log.debug("exposing namespaces['%s'].commands['%s'] from '%s'" % \
            (namespace, func.__name__, func.__module__))
            
        name = re.sub('_', '-', func.__name__)
        if not namespace in namespaces:
            raise CementRuntimeError, \
                "The namespace '%s' is not defined!" % namespace
        
        func = render(template)(func)        
        
        cmd = {
            'is_hidden' : kwargs.get('is_hidden', False),
            'func' : func
            }
            
        namespaces[namespace].commands[name] = cmd
        return func
    return decorate