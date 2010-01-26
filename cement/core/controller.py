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
    controller = namespaces[namespace].controller()
    func = getattr(controller, func)(*args, **kwargs)
                      
class expose2(object):
    """
    Decorator function for plugins to expose commands.  Used as:
    
    Arguments:
    
        template  -- A template in python module form 
                    (i.e 'myapp.templates.mytemplate')
        
        namespace -- The namespace to expose the command in.  Default: root
    
    Optional Keyword Arguments:
    
        is_hidden -- True/False whether command should display on --help.
        
    Usage: 
    
        @expose('app_module.view.template', namespace='namespace')
        def mycommand(self):
            ...
    """
    def __init__(self, template=None, namespace='root', **kwargs):
        # These get set in __call__
        self.func = None
        self.json_func = None
        
        self.template = template
        self.namespace = namespace
        self.tmpl_module = None
        self.tmpl_file = None
        self.engine = 'genshi'
        self.config = namespaces['root'].config
        self.is_hidden = kwargs.get('is_hidden', False)
        
        if self.template == 'json':
            self.engine = 'json'
            self.template = None

        elif self.template:
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
        mymod = __import__(func.__module__, globals(), locals(), 
                           ['__controller__'], -1)

        try:
            controller = mymod.__controller__
        except AttributeError, e:
            raise CementRuntimeError, "function '%s': %s" % (func.__name__, str(e))
        
        self.func = func
        self.json_func = self.func
        
        log.debug("exposing namespaces['%s'].commands['%s'] from '%s'" % \
                 (self.namespace, self.func.__name__, self.func.__module__))
                
        # First for the template
        name = re.sub('_', '-', self.func.__name__)
        if self.template:
            cmd = {
                'is_hidden' : self.is_hidden,
                'func' : self.func.__name__,
                'module' : self.json_func.__module__,
                'controller' : controller
                }

            # Set the command info in the dest namespace
            namespaces[self.namespace].commands[name] = cmd
            
            # Set the attr on the controller with the new fun
            print namespaces
            setattr(namespaces[con_namespace].controller, self.func)

        # Then for setattr for the json command
        
        name = "%s.json" % name
      
        json_cmd = {
            'is_hidden' : True,
            'func' : self.json_func.__name__,
            'module' : self.json_func.__module__,
            'controller' : controller
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
            return func
        return wrapper
        
        
class expose(object):
    """
    Decorator function for plugins to expose commands.  Used as:
    
    Arguments:
    
        template  -- A template in python module form 
                    (i.e 'myapp.templates.mytemplate')
        
        namespace -- The namespace to expose the command in.  Default: root
    
    Optional Keyword Arguments:
    
        is_hidden -- True/False whether command should display on --help.
        
    Usage: 
    
        @expose('app_module.view.template', namespace='namespace')
        def mycommand(self):
            ...
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
        mymod = __import__(func.__module__, globals(), locals(), 
                           ['__controller__'], -1)

        try:
            controller = mymod.__controller__
        except AttributeError, e:
            raise CementRuntimeError, "function '%s': %s" % (func.__name__, str(e))
        
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
            #'module' : func.__module__,
            #'controller' : controller
            }

        # Set the command info in the dest namespace
        namespaces[self.namespace].commands[cmd_name] = cmd
        self.func = render(self.template)(self.func)
        return self.func
      