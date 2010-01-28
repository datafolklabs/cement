"""Methods and classes to handle Cement namespace support."""

from cement import namespaces
from cement.core.exc import CementRuntimeError
from cement.core.configuration import get_default_plugin_config
from cement.core.opt import init_parser

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
    def __init__(self, label, version, required_api, **kw):
        self.label = label
        self.version = version
        self.required_api = required_api
        self.description = kw.get('description', '')
        self.commands = kw.get('commands', {})
        self.controller = kw.get('controller', None)
        self.is_hidden = kw.get('is_hidden', False)
        
        self.config = get_default_plugin_config()
        if kw.get('config', None):
            self.config.update(kw['config'])

        if not kw.get('banner'):
            banner = "%s version %s" % (self.label, self.version)
        else:
            banner = kw.get('banner')
        self.options = kw.get('options', init_parser(banner=banner))
            
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
