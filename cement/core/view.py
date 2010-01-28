"""Methods and classes that enable Cement templating support."""

import os
import re
import json
import inspect
from pkgutil import get_data

from cement import namespaces, SAVED_STDOUT, SAVED_STDERR, \
                   buf_stdout, buf_stderr
from cement.core.exc import CementRuntimeError
from cement.core.log import get_logger
from genshi.template import NewTextTemplate

log = get_logger(__name__)

class render(object):
    """
    Class decorator to render data with Genshi text formatting engine or json.
    Called when the function is decorated, sets up the engine and template for 
    later use.  If not passed a template, render will do nothing (unless 
    --json is passed, by which json is returned).
    
    *Note: This is called form the cement.core.controller.expose() decorator 
    and likely shouldn't ever be needed to call directly.*
    
    Keywork arguments:
    
        template
            The module path to the template (default: None)
                
    """
    def __init__(self, template=None):
        self.func = None
        self.template = template
        self.tmpl_module = None
        self.tmpl_file = None
        self.engine = 'genshi'
        self.config = namespaces['root'].config
        
        if self.template == 'json':
            self.engine = 'json'
            self.template = None

        elif self.template:
            # Mock up the template path
            parts = template.split('.')
            self.tmpl_file = "%s.txt" % parts.pop() # the last item is the file            
            self.tmpl_module = '.'.join(parts) # left over in between
            
    def __call__(self, func):
        """
        Called when the command function is actually run.  Expects a 
        dictionary in return from the function decorated in __init__.
        
        """
        self.func = func
        def wrapper(*args, **kw):  
            log.debug("decorating '%s' with '%s:%s'" % \
                (func.__name__, self.engine, self.template))      
            
            res = self.func(*args, **kw)
            if not res:
                res = dict()
                
            # FIX ME: Is there a better way to jsonify classes?
            if self.engine == 'json':
                namespaces['root'].config['output_engine'] = 'json'
                safe_res = {}
                for i in res:
                    try:
                        getattr(res[i], '__dict__')
                        safe_res[i] = res[i].__dict__
                    except AttributeError, e:
                        safe_res[i] = res[i]
                
                safe_res['stdout'] = buf_stdout.buffer
                safe_res['stderr'] = buf_stderr.buffer
                try:
                    SAVED_STDOUT.write(json.dumps(safe_res))
                except TypeError, e:
                    safe_res = {}
                    safe_res['errors'] = {'TypeError' : str(e)}
                    SAVED_STDOUT.write(json.dumps(safe_res))
            
            elif self.engine == 'genshi':  
                namespaces['root'].config['output_engine'] = 'genshi'
                if self.template:  
                    # FIX ME: Pretty sure genshi has better means of doing 
                    # this, but couldn't get it to work.
                    tmpl_text = get_data(self.tmpl_module, self.tmpl_file)
                    tmpl = NewTextTemplate(tmpl_text)
                    print tmpl.generate(**res).render()
        return wrapper
        