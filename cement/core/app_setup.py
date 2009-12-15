"""Cement methods to setup the framework for applications using it."""
import sys, os
import re
from pkg_resources import get_distribution
from optparse import OptionParser, IndentedHelpFormatter

from cement import plugins as cement_plugins
from cement import hooks, namespaces
from cement.core.log import setup_logging, get_logger
from cement.core.options import get_options, Options
from cement.core.exc import CementConfigError, CementRuntimeError, \
                            CementArgumentError
from cement.core.configuration import set_config_opts_per_file, \
                                      validate_config, CementNamespace, \
                                      define_namespace, get_default_config, \
                                      set_config_opts_per_cli_opts

CEMENT_ABI = "20091211"

log = get_logger(__name__)

class CementCommand(object):
    def __init__(self, cli_opts=None, cli_args=None):
        self.is_hidden = False # whether to display in command list at all
        self.is_global = False # whether to display in global command list
        self.cli_opts = cli_opts
        self.cli_args = cli_args
    
    def help(self):
        """Display command help information."""
        print "No help information available."
    
    def run(self):
        """Run the command actions."""
        print "No actions have been defined for this command."
        

class CementPlugin(CementNamespace):
    def __init__(self, *args, **kwargs):
        CementNamespace.__init__(self, *args, **kwargs)


        
def get_abi_version():
    return CEMENT_ABI
    
def ensure_abi_compat(module_name, required_abi):
    if int(required_abi) == int(CEMENT_ABI):
        pass
    else:
        raise CementRuntimeError, \
            "%s requires abi version %s which differs from cement(abi) %s." % \
                (module_name, required_abi, CEMENT_ABI)
    
    
def define_hook(namespace):
    """
    Define a hook namespace that plugins can register hooks in.
    """
    if hooks.has_key(namespace):
        raise CementRuntimeError, "Hook name '%s' already defined!" % namespace
    hooks[namespace] = []
    
    
def register_hook(**kwargs):
    """
    Decorator function for plugins to register hooks.  Used as:
    
    @register_hook()
    def my_hook():
        ...
    """
    def decorate(func):
        if not hooks.has_key(func.__name__):
            #raise CementRuntimeError, "Hook name '%s' is not define!" % func.__name__
            log.warn("Hook name '%s' is not define!" % func.__name__)
            return func
        # (1) is the list of registered hooks in the namespace
        hooks[func.__name__].append(
            (int(kwargs.get('weight', 0)), func.__name__, func)
        )
        return func
    return decorate


def run_hooks(namespace, *args, **kwargs):
    """
    Run all defined hooks in the namespace.  Returns a list of return data.
    """
    if not hooks.has_key(namespace):
        CementRuntimeError, "Hook name '%s' is not defined!" % namespace
    hooks[namespace].sort() # will order based on weight
    for hook in hooks[namespace]:
        res = hook[2](*args, **kwargs)
        
        # FIXME: Need to validate the return data somehow
        yield res


#def define_command(namespace):
#    """
#    Define a command namespace that plugins can register commands in.
#    """
#    if namespaces[namespace].commands.has_key(namespace):
#        #raise CementRuntimeError, "Command namespace '%s' already defined!" % namespace
#        return
#    commands[namespace] = {}
    
    
def register_command(name=None, namespace='global', **kwargs):
    """
    Decorator function for plugins to register commands.  Used as:
    
    @register_command(namespace='namespace')
    class MyCommand(CementCommand):
        ...
    """
    assert name, "Command name is required!"
    def decorate(func):
        if not namespace in namespaces:
            raise CementRuntimeError, "The namespace '%s' is not defined!" % namespace
        setattr(func, 'is_hidden', kwargs.get('is_hidden', False))
        namespaces[namespace].commands[name] = func
        return func
    return decorate
        
# FIXME: This method is so effing ugly.
def run_command(command_name):
    """
    Run the command or namespace-subcommand.
    """
    
    command_name = command_name.lstrip('*') 
    if command_name in namespaces.keys():
        namespace = command_name
    else:
        namespace = 'global'
    
    commands = namespaces[namespace].commands
    
    if re.match('(.*)-help', command_name) and command_name.rstrip('-help') in namespaces.keys():   
        namespace = command_name.rstrip('-help') 
        raise CementArgumentError, \
            "'%s' is a *namespace, not a command.  See '%s --help' instead." % \
                (namespace, namespace)
        
    (cli_opts, cli_args) = parse_options(namespace=namespace)
    set_config_opts_per_cli_opts(namespace, cli_opts)
    
    # FIX ME: need a global_pre_command_hook here so that clibasic can
    # look for -C and if so, parse the passed config files into the dict.
    for res in run_hooks('global_post_options_hook'):
        pass
    
    if namespace == 'global':
        actual_cmd = command_name
    else:
        try:
            actual_cmd = cli_args[1]
        except IndexError:
            raise CementArgumentError, \
                "Missing sub-command.  See '%s --help?" % (namespace)
    
    m = re.match('(.*)-help', actual_cmd)
    if m:
        if namespaces[namespace].commands.has_key(m.group(1)):
            cmd = namespaces[namespace].commands[m.group(1)](cli_opts, cli_args)
            cmd.help()
        else:
            raise CementArgumentError, \
                "Unknown command '%s'.  See --help?" % actual_cmd
            
    elif namespaces[namespace].commands.has_key(actual_cmd):
        cmd = namespaces[namespace].commands[actual_cmd](cli_opts, cli_args)
        cmd.run()
                        
    else:
        raise CementArgumentError, "Unknown command, see --help?"
    
    
def register_plugin(**kwargs):
    """
    Decorator function to register plugin namespace.  Used as:
    
    @register_plugin()
    class MyPlugin(CementPlugin):
        ...
    """
    def decorate(func):
        ensure_abi_compat(func.__name__, func().required_abi)
        plugin_name = func.__module__.split('.')[-1]
        define_namespace(plugin_name, func())
        return func
    return decorate
    

def register_default_hooks():
    # define default hooks
    define_hook('global_options_hook')
    define_hook('global_post_options_hook')
        
def lay_cement(default_app_config=None, version_banner=None):
    """
    Primary method to setup an application for Cement.  
    
    Arguments:
    
    config => dict containing application config.
    version_banner => Option txt displayed for --version
    """    
    global namespaces, log
    
    vb = version_banner    
    if not version_banner:
        vb = """%s version %s""" % (
            default_app_config['app_name'],
            get_distribution(default_app_config['app_egg_name']).version
            )
        
    namespace = CementNamespace(
        label = 'global',
        version = get_distribution(default_app_config['app_egg_name']).version,
        required_abi = CEMENT_ABI,
        config = get_default_config(),
        version_banner = vb,
        )
    define_namespace('global', namespace)
    namespaces['global'].config.update(default_app_config)
    validate_config(namespaces['global'].config)
    
    register_default_hooks()
    
    for cf in namespaces['global'].config['config_files']:
        set_config_opts_per_file('global', 
                                 namespaces['global'].config['app_module'], 
                                 cf)
    # initial logger
    setup_logging('cement', clear_loggers=True)
    log = get_logger(__name__)                             
    
    load_all_plugins()
    setup_logging('cement', clear_loggers=True)
    setup_logging(namespaces['global'].config['app_module'])
    


def load_plugin(plugin):
    """
    Load a cement type plugin.  
    
    Arguments:
    
    plugin  => Name of the plugin to load.
    """
    global namespaces
    config = namespaces['global'].config
    
    if config.has_key('show_plugin_load') and config['show_plugin_load']:
        print 'loading %s plugin' % plugin
    
    try: 
        app_module = __import__(config['app_module'])
    except ImportError, e:
        raise CementConfigError, e
        
    try:
        plugin_module = __import__('%s.plugins' % config['app_module'], globals(), locals(),
               [plugin], -1)
        getattr(plugin_module, plugin)
    except AttributeError, e:
        try:
            plugin_module = __import__('cement.plugins', globals(), locals(),
                   [plugin], -1)
            getattr(plugin_module, plugin)
        except AttributeError, e:
            raise CementRuntimeError, "Failed loading plugin '%s', possibly syntax errors?" % plugin
        
    plugin_config_file = os.path.join(
        namespaces['global'].config['plugin_config_dir'], '%s.plugin' % plugin
        )
        
    set_config_opts_per_file(plugin, plugin, plugin_config_file)
    
                       
def load_all_plugins():
    """
    Attempt to load all enabled plugins.  Passes the existing config and 
    options object to each plugin and allows them to add/update each.
    """
    global namespaces

    for plugin in namespaces['global'].config['enabled_plugins']:
        load_plugin(plugin)
        
    for res in run_hooks('global_options_hook'):
        for opt in res._get_all_options(): 
            if opt.get_opt_string() == '--help':
                pass
            else:
                namespaces['global'].options.add_option(opt)
        
        
def parse_options(namespace='global'): 
    """
    The actual method that parses the command line options and args.  
    
    Arguments:
    
    config => dict containing the application configurations.
    options_obj => The options object used to pass the parser around.
    commands => Plugin commands to be added to the --help output.
    
    Returns => a tuple of (options, args)
    """
    global namespaces

    if namespaces[namespace].config.has_key('merge_global_options') and \
       namespaces[namespace].config['merge_global_options']:
        for opt in namespaces['global'].options._get_all_options(): 
            if opt.get_opt_string() == '--help':
                pass
            elif opt.get_opt_string() == '--version':
                pass
            else:
                namespaces[namespace].options.add_option(opt)
    
    cmd_txt = ''
    line = '    '
    if namespaces[namespace].commands:
        for c in namespaces[namespace].commands:    
            if c.endswith('-help') or namespaces[namespace].commands[c].is_hidden:
                pass
            else:
                if line == '    ':
                    line += '%s' % c
                elif len(line) + len(c) < 55:
                    line += ' - %s' % c
                else:
                    cmd_txt += "%s \n" % line
                    line = '    '

    if namespace == 'global':
        for nam in namespaces: 
            if nam != 'global' and namespaces[nam].commands:
                if line == '    ':
                    line += '*%s' % nam
                elif len(line) + len(nam) < 55:
                    line += ' - *%s' % nam
                else:
                    cmd_txt += "%s \n" % line
                    line = '    '

    if line != '    ':
        cmd_txt += "%s\n" % line
    
    if namespace != 'global':
        namespace_txt = ' %s' % namespace
        cmd_type_txt = 'SUBCOMMAND'
    else:
        namespace_txt = ''
        cmd_type_txt = 'COMMAND'
    
    script = os.path.basename(sys.argv[0])
    namespaces[namespace].options.usage = """  %s%s [%s] --(OPTIONS)

Commands:  
%s
    
Help?  try [%s]-help""" % (script, namespace_txt, cmd_type_txt, cmd_txt, cmd_type_txt)

    (opts, args) = namespaces[namespace].options.parse_args()
    
    return (opts, args)
