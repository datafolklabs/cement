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
    
        template  -- A template in python module form 
                    (i.e 'myapp.templates.mytemplate')
        
        namespace -- The namespace to expose the command in.  Default: global
    
    Optional Keyword Arguments:
    
        is_hidden -- True/False whether command should display on --help.
        
    Usage: 
    
        @expose('app_module.view.template', namespace='namespace')
        def mycommand(self):
            ...
    """
    def decorate(func):
        log.debug("exposing namespaces['%s'].commands['%s'] from '%s'" % \
            (namespace, func.__name__, func.__module__))
        
        json_func = func
        
        # first for the template
        name = re.sub('_', '-', func.__name__)
        if template == 'json':
            name = "%s.json" % func.__name__
            
        if not namespace in namespaces:
            raise CementRuntimeError, \
                "The namespace '%s' is not defined!" % namespace

        func = render(template)(func)        
        
        cmd = {
            'is_hidden' : kwargs.get('is_hidden', False),
            'func' : func
            }

        namespaces[namespace].commands[name] = cmd
    
        # Then for json
        name = re.sub('_', '-', json_func.__name__)
        name = "%s.json" % name
    
        json_func = render('json')(json_func)        
    
        json_cmd = {
            'is_hidden' : True,
            'func' : json_func
            }
        namespaces[namespace].commands[name] = json_cmd
        
        return func
    return decorate