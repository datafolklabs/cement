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

def get_namespace(namespace):
    """
    Return the namespace object whose label is 'namespace'.
    
    Required Arguments:
    
        namespace
            The label of the namespace object to return
    
    """
    if namespaces.has_key(namespace):
        return namespaces[namespace]
    else:
        log.fatal("the namespace '%s' doesn't exist" % namespace)

def get_config(namespace='root'):
    """Get a namespace's config dictionary.  Returns a ConfigObj object.
    
    Optional Arguments:
    
        namespace
            The namespace to pull the config object from.  Default: 'root'.
    
    """    
    if namespaces.has_key(namespace):
        return namespaces[namespace].config.dict()
    else:
        log.fatal("the namespace '%s' doesn't exist" % namespace)
    
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
            A configobj object (default: None).  A basic default config will
            be created if none is passed.  For advanced configurations such
            as using a configspec or what have you can be done by passing in
            the configobj object.
        banner
            A version banner to display for --version (default: '')
            
    """
    def __init__(self, label, **kw):
        if not label == 'root':
            app_name = namespaces['root'].config['app_name']
            self.version = kw.get('version', get_distribution(app_name).version)
            self.required_api = kw.get('required_api', namespaces['root'].required_api)
            self.provider = kw.get('provider', namespaces['root'].config['app_module'])
        else:
            self.version = kw.get('version', None)
            self.required_api = kw.get('required_api', None)
            self.provider = kw.get('provider', None)
            
        try:
            assert self.version, "A namespace version is required!"
            assert self.required_api, "A required_api version is required!"
            assert self.provider, "A namespace provider is required!"
        except AssertionError, e:
            raise CementRuntimeError, e.__str__()
            
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
    """
    Wraps up defining a namespace, as well as revealing the actual controller
    object (as it is passed as a string).
    
    Require Arguments:
    
        namespace_obj
            Namespace object that is fully established (and ready to be 
            added to the global namespaces dictionary)
            
    Usage:
    
    .. code-block:: python
    
        from cement.core.namespace import CementNamespace, register_namespace

        example = CementNamespace('example', controller='ExampleController')
        example.config['foo'] = 'bar'
        example.options.add_option('-F', '--foo', action='store',
            dest='foo', default=None, help='Example Foo Option')
        register_namespace(example)
        
    """
    ensure_api_compat(namespace_obj.label, namespace_obj.required_api)
    define_namespace(namespace_obj.label, namespace_obj)
    
    # Reveal the controller object.
    base = namespace_obj.provider
    mymod = __import__('%s.controllers.%s' % (base, namespace_obj.label), 
                       globals(), locals(), [namespace_obj.controller], -1)
    cont = getattr(mymod, namespace_obj.controller)                  
    namespaces[namespace_obj.label].controller = cont
    for file in namespaces['root'].config['config_files']:
        set_config_opts_per_file(namespace_obj.label, namespace_obj.label, 
                                 file)
        