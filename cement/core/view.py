"""Methods and classes that enable Cement templating support."""

import sys
import os
import re
import jsonpickle
import inspect
from pkgutil import get_data

from cement import handlers
from cement import namespaces, SAVED_STDOUT, SAVED_STDERR
from cement import buf_stdout, buf_stderr
from cement.core.exc import CementRuntimeError
from cement.core.log import get_logger
from genshi.template import NewTextTemplate

log = get_logger(__name__)

def render_genshi_output(return_dict, template_content=None):
    log.debug("rendering genshi output")
    if template_content:  
        tmpl = NewTextTemplate(template_content)
        return tmpl.generate(**return_dict).render()
    else:
        log.debug('unable to render genshi output without template_content.')
        return return_dict

def render_json_output(return_dict, template_content=None):
    log.debug("rendering json output")
    return_dict['stdout'] = buf_stdout.buffer
    return_dict['stderr'] = buf_stderr.buffer
    return jsonpickle.encode(return_dict, unpicklable=False)
    
class render(object):
    """
    Class decorator to render data with Genshi text formatting engine or json.
    Called when the function is decorated, sets up the engine and template for 
    later use.  If not passed a template, render will do nothing (unless 
    --json is passed, by which json is returned).
    
    *Note: This is called form the cement.core.controller.expose() decorator 
    and likely shouldn't ever be needed to call directly.*
    
    *Note: If 'output_file' is passed in the return dictionary from func, then
    the output is written to the specified file rather than STDOUT.*
    
    Keywork arguments:
    
        template
            The module path to the template (default: None)
                
    """
    def __init__(self, output_handler, template=None):
        self.func = None
        self.template = template
        self.tmpl_module = None
        self.tmpl_file = None
        self.config = namespaces['root'].config
        self.output_handler = output_handler
            
        # ?
        #if self.template and self.template == 'json':
        #    self.handler = 'json'        
        #elif self.template:
        if self.template:
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
            # honor output_handler_override
            if self.config['output_handler_override']:
                self.output_handler = self.config['output_handler_override']

            log.debug("decorating '%s' with '%s:%s'" % \
                (func.__name__, self.output_handler, self.template))  
                
            res = self.func(*args, **kw)
            
            out = SAVED_STDOUT
            out_content = ''
            tmpl_content = None
            
            if not res:
                res = dict()
            if type(res) != dict:
                raise CementRuntimeError, "Controller functions must return type dict()."
            
            if self.template:  
                template_content = get_data(self.tmpl_module, self.tmpl_file)
            
            if self.output_handler in handlers['output_handlers']:
                handler = handlers['output_handlers'][self.output_handler]
                namespaces['root'].config['output_handler'] = self.output_handler
                out_txt = handler(res, template_content)
                
                if res.has_key('output_file') and res['output_file']:
                    f = open(res['output_file'], 'w+')
                    f.write(output)
                    f.close()
                elif out and self.config['log_to_console']:
                    out.write(out_txt)

            else:
                raise CementRuntimeError, "Handler name '%s' does not exist in handlers['output_handlers']." % \
                                           self.output_handler        
        return wrapper