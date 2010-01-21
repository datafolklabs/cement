"""Methods and classes that enable Cement templating support."""

import os
from sys import stdout
import re
import json
import inspect

from cement import namespaces
from cement.core.log import get_logger
from genshi.template import NewTextTemplate

log = get_logger(__name__)

class render(object):
    """
    Class decorator to render data with Genshi text formatting engine or json.
    """
    template = None
    engine = 'genshi'
    
    def __init__(self, template=None):
        """
        Called when the function is decorated, sets up the engine and 
        template for later use.  If not passed a template, render will do 
        nothing (unless --json is passed, by which json is returned).
        
        Keywork arguments:
        template -- The module path to the template (default: None)
        
        Usage:
            @expose('myapp.templates.myplugin.template_name')
            def mycommand(self, *args, *kwargs)
                ...
                
        """
        self.config = namespaces['global'].config
        
        if template == 'json':
            self.engine = 'json'
            self.template = None

        elif template:
            # Mock up the template path
            t = re.sub('%s\.' % self.config['app_module'], '', template)
            t = re.sub('\.', '/', t)
        
            self.template = os.path.join(self.config['app_basepath'], 
                                         '%s.txt' % t)
            
    def __call__(self, func):
        """
        Called when the command function is actually run.  Expects a 
        dictionary in return from the function decorated in __init__.
        
        """
        def wrapper(*args, **kw):  
            log.debug("decorating '%s' with '%s:%s'" % \
                (func.__name__, self.engine, self.template))      
            res = func(func, *args, **kw)
            
            # FIX ME: Is there a better way to jsonify classes?
            if self.engine == 'json':
                safe_res = {}
                for i in res:
                    try:
                        getattr(res[i], '__dict__')
                        safe_res[i] = res[i].__dict__
                    except AttributeError, e:
                        safe_res[i] = res[i]
                print json.dumps(safe_res)
            
            elif self.engine == 'genshi':  
                if self.template:  
                    # FIX ME: Pretty sure genshi has better means of doing 
                    # this, but couldn't get it to work.
                    tmpl_text = open(self.template).read()
                    tmpl = NewTextTemplate(tmpl_text)
                    print tmpl.generate(**res).render()
        return wrapper
        