"""Methods and classes that enable Cement templating support."""

import sys
import os
import re
import jsonpickle
import yaml
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
    --json or --yaml is passed, by which json or yaml is returned, respectively).
    
    *Note: This is called form the cement.core.controller.expose() decorator 
    and likely shouldn't ever be needed to call directly.*
    
    *Note: If 'output_file' is passed in the return dictionary from func, then
    the output is written to the specified file rather than STDOUT.*
    
    Keywork arguments:
    
        template
            The module path to the template (default: None)
                
    """
    def __init__(self, engine_template=None):
        self.func = None
        self.template = None
        self.tmpl_module = None
        self.tmpl_file = None
        self.config = namespaces['root'].config
        self.engine = self.config['output_engine']
        
        if engine_template:
            parts = engine_template.split(':')
            if len(parts) >= 2:
                self.engine = parts[0]
                self.template = parts[1]
            elif len(parts) == 1:
                self.template = parts[0]
            else:
                raise CementRuntimeError, "Invalid engine:template identifier."
            
            if self.template and self.template == 'json':
                self.engine = 'json'

            elif self.template and self.template == 'yaml':
                self.engine = 'yaml'

            elif self.template:
                # Mock up the template path
                parts = self.template.split('.')
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
            output = ''
            output_handler = SAVED_STDOUT
            if not res:
                res = dict()
                
            if self.engine == 'json':
                namespaces['root'].config['output_engine'] = 'json'
                res['stdout'] = buf_stdout.buffer
                res['stderr'] = buf_stderr.buffer
                output = jsonpickle.encode(res, unpicklable=False)

            if self.engine == 'yaml':
                namespaces['root'].config['output_engine'] = 'yaml'
                res['stdout'] = buf_stdout.buffer
                res['stderr'] = buf_stderr.buffer
                output = yaml.dump(res)
            
            elif self.engine == 'genshi':  
                namespaces['root'].config['output_engine'] = 'genshi'
                if self.template:  
                    # FIX ME: Pretty sure genshi has better means of doing 
                    # this, but couldn't get it to work.
                    tmpl_text = get_data(self.tmpl_module, self.tmpl_file)
                    tmpl = NewTextTemplate(tmpl_text)
                    output = tmpl.generate(**res).render()
                    
            if res.has_key('output_file') and res['output_file']:
                f = open(res['output_file'], 'w+')
                f.write(output)
                f.close()
            elif output and self.config['log_to_console']:
                output_handler.write(output)
                
        return wrapper
        