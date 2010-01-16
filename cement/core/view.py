"""Methods and classes that enable Cement templating support."""

import os
import re
import json

from cement import namespaces
from cement.core.log import get_logger
from genshi.template import NewTextTemplate

log = get_logger(__name__)

class render(object):
    """
    Render data with Genshi text formatting engine.
    """
    template = None
    engine = 'genshi'
    
    def __init__(self, template=None):
        self.config = namespaces['global'].config
        
        if template == 'json':
            self.engine = 'json'
            self.template = None

        # mock up the template
        if template:
            t = re.sub('%s\.' % self.config['app_module'], '', template)
            t = re.sub('\.', '/', t)
        
            self.template = os.path.join(self.config['app_basepath'], 
                                         '%s.txt' % t)
            
    def __call__(self, func):
        def wrapper(*args, **kw):  
            log.debug("decorating '%s' with '%s:%s'" % \
                (func.__name__, self.engine, self.template))      
            res = func(func, *args, **kw)
            
            if self.engine == 'json':
                print json.dumps(res)
            
            elif self.engine == 'genshi':  
                if self.template:  
                    # FIX ME: Pretty sure genshi has better means of doing this, but
                    # couldn't get it figured out.
                    tmpl_text = open(self.template).read()
                    tmpl = NewTextTemplate(tmpl_text)
                    print tmpl.generate(**res).render()
        return wrapper