
from cement import namespaces
from cement.core.opt import init_parser

class CementNamespace(object):
    def __init__(self, label, version, required_abi, **kw):
        self.label = label
        self.version = version
        self.required_abi = required_abi
        self.description = kw.get('description', '')
        self.commands = kw.get('commands', {})
        self.config = kw.get('config', {'config_source': ['defaults']})
        self.is_hidden = kw.get('is_hidden', False)
        
        if not kw.get('version_banner'):
            vb = "%s version %s" % (self.label, self.version)
        else:
            vb = kw.get('version_banner')
        self.options = kw.get('options', init_parser(version_banner=vb))
            
def define_namespace(namespace, namespace_obj):
    """
    Define a namespace for commands, options, configuration, etc.  
    
    Arguments:
    
    namespace => label of the namespace
    namespace_obj => CementNamespace object
    """
    if namespaces.has_key(namespace):
        raise CementRuntimeError, "Namespace '%s' already defined!" % namespace
    namespaces[namespace] = namespace_obj