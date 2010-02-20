"""Methods and classes to handle Cement namespace support."""

from pkg_resources import get_distribution

from cement import namespaces
from cement.core.log import get_logger
from cement.core.configuration import ensure_api_compat
from cement.core.exc import CementRuntimeError
from cement.core.configuration import get_default_namespace_config, \
                                      set_config_opts_per_file
from cement.core.opt import init_parser

log = get_logger(__name__)

def register_namespaceOLD(**kwargs):
    """
    Decorator function to register a namespace.  Alternative to registering
    a plugin, but essentially the same thing.  
    
    Usage:    
    
    .. code-block:: python

        from cement.core.namespace import CementNamespace, register_namespace
            
        @register_namespace()
        class ExampleNamespace(CementNamespace):
            def __init__(self):
                CementNamespace.__init__(self,
                    label='example',
                    required_api='0.5-0.6:20100115',
                    controller = 'ExampleController'
                    )    
    
    *Note: 'ExampleController' should match up with the controller object in
    myapp.controllers.example.ExampleController.*  The path to the controller
    module is determined by the 'label' of the namespace.  
    
    """
    def decorate(func):
        """
        Decorate a plugin class and add the namespace to global namespaces
        dictionary.
        
        """
        nms = func.__module__.split('.')
        inst_func = func()
        ensure_api_compat(func.__name__, inst_func.required_api)
        define_namespace(inst_func.label, inst_func)
        
        base = namespaces['root'].config['app_module']
        mymod = __import__('%s.controllers.%s' % (base, inst_func.label), 
                           globals(), locals(), [inst_func.controller], -1)
        controller = getattr(mymod, inst_func.controller)                  
        namespaces[inst_func.label].controller = controller
        return func
    return decorate
    
    
class CementNamespace(object):
    """
    Class that handles plugins and namespaces.
    
    Required Arguments:
        
        label
            Namespace label.  Class is stored in the global 'namespaces' 
            dict as namespaces['label'].
        version
            The version of the application.
        required_api
            The required Cement API the application was built on.
        
    Optional Keyword Arguments:
        
        description
            Description of the plugin/namespace (default: '')
        commands
            A dict of command functions (default: {})
        is_hidden
            Boolean, whether command should display in --help output 
            (default: False)
        config
            A config dict (default: None)
        banner
            A version banner to display for --version (default: '')
            
    """
    def __init__(self, label, **kw):
        if not label == 'root':
            app_module = namespaces['root'].config['app_module']
            self.version = kw.get('version', get_distribution(app_module).version)
            self.required_api = kw.get('required_api', namespaces['root'].required_api)
        else:
            self.version = kw.get('version', None)
            self.required_api = kw.get('required_api', None)
            
        self.label = label
        self.description = kw.get('description', '')
        self.commands = kw.get('commands', {})
        self.controller = kw.get('controller', None)
        self.is_hidden = kw.get('is_hidden', False)
        
        self.config = get_default_namespace_config()
        if kw.get('config', None):
            self.config.update(kw['config'])

        if kw.get('banner', None):
            self.banner = kw['banner']
        else:
            self.banner = "%s version %s" % (self.label, self.version)
            
        self.options = kw.get('options', init_parser(banner=self.banner))
            
def define_namespace(namespace, namespace_obj):
    """
    Define a namespace for commands, options, configuration, etc.  
    
    Required Arguments:
    
        namespace
            Label of the namespace
        namespace_obj
            CementNamespace object.  Stored in global 'namespaces' dict as 
            namespaces['namespace']
                     
    """
    if namespaces.has_key(namespace):
        raise CementRuntimeError, "Namespace '%s' already defined!" % namespace
    namespaces[namespace] = namespace_obj
    log.debug("namespace '%s' initialized from '%s'." % \
             (namespace, namespace_obj.__module__))

def register_namespace(namespace_obj):
    ensure_api_compat(namespace_obj.__module__, namespace_obj.required_api)
    define_namespace(namespace_obj.label, namespace_obj)
    
    # Reveal the controller object.
    base = namespaces['root'].config['app_module']
    mymod = __import__('%s.controllers.%s' % (base, namespace_obj.label), 
                       globals(), locals(), [namespace_obj.controller], -1)
    cont = getattr(mymod, namespace_obj.controller)                  
    namespaces[namespace_obj.label].controller = cont
    for file in namespaces['root'].config['config_files']:
        set_config_opts_per_file(namespace_obj.label, namespace_obj.label, file)
        