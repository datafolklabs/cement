"""Methods and classes to handle Cement Controller functions."""
import re

from cement import namespaces
from cement.core.log import get_logger
from cement.core.exc import CementRuntimeError
#from cement.core.view import render
    
log = get_logger(__name__)

class CementController(object):
    """Currently just a place holder for more featureful controller."""
    pass
              
class expose(object):
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
    def __init__(self, template=None, namespace='global', **kwargs):
        self.func = None
        self.json_func = None
        self.template = template
        self.namespace = namespace
        self.tmpl_module = None
        self.tmpl_file = None
        self.engine = 'genshi'
        self.config = namespaces['global'].config
        self.is_hidden = kwargs.get('is_hidden', False)
        
        #func = render(template)(func)        
        if self.template == 'json':
            self.engine = 'json'
            self.template = None

        elif self.template:
            # Mock up the template path
            parts = template.split('.')
            self.tmpl_file = "%s.txt" % parts.pop() # the last item is the file            
            self.tmpl_module = '.'.join(parts) # left over in between
        
        if not self.namespace in namespaces:
            raise CementRuntimeError, \
                "The namespace '%s' is not defined!" % self.namespace
                        
    def __get__(self, obj, type=None):
        print 'IN GET'
        if obj is None:
            return self
        new_func = self.func.__get__(obj, type)
        return self.__class__(new_func)
        
    def __call__(self, func):
        self.func = func
        self.json_func = self.func
        print self.func
        log.debug("exposing namespaces['%s'].commands['%s'] from '%s'" % \
                 (self.namespace, self.func.__name__, self.func.__module__))
                
        # First for the template
        if self.template:
            name = re.sub('_', '-', self.func.__name__)
            cmd = {
                'is_hidden' : self.is_hidden,
                'func' : self.func
                }

            namespaces[self.namespace].commands[name] = cmd

        # Then for json
        name = re.sub('_', '-', self.json_func.__name__)
        name = "%s.json" % name

        #self.json_func = render('json')(self.json_func)        
        json_cmd = {
            'is_hidden' : True,
            'func' : self.json_func
            }
        namespaces[self.namespace].commands[name] = json_cmd
        
        # This is what actually gets called when the command is run
        def wrapper(*args, **kwargs):
            log.debug("decorating '%s' with '%s:%s'" % \
                (self.func.__name__, self.engine, self.template))      
        
            res = self.func(*args, **kwargs)
        
            # FIX ME: Is there a better way to jsonify classes?
            if self.engine == 'json':
                safe_res = {}
                for i in res:
                    try:
                        getattr(res[i], '__dict__')
                        safe_res[i] = res[i].__dict__
                    except AttributeError, e:
                        safe_res[i] = res[i]
            
                safe_res['stdout'] = buf_stdout.buffer
                safe_res['stderr'] = buf_stderr.buffer
                SAVED_STDOUT.write(json.dumps(safe_res))
        
            elif self.engine == 'genshi':  
                if self.template:  
                    # FIX ME: Pretty sure genshi has better means of doing 
                    # this, but couldn't get it to work.
                    tmpl_text = get_data(self.tmpl_module, self.tmpl_file)
                    tmpl = NewTextTemplate(tmpl_text)
                    print tmpl.generate(**res).render()