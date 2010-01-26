"""These methods and classes controller how commands are parsed and run."""

import re

from cement import namespaces
from cement.core.log import get_logger
from cement.core.hook import run_hooks
from cement.core.opt import parse_options
from cement.core.configuration import set_config_opts_per_cli_opts
from cement.core.controller import run_controller_command
from cement.core.exc import CementArgumentError

log = get_logger(__name__)
        
# FIXME: This method is so effing ugly.
def run_command(cmd_name=None):
    """
    Run the command or namespace-subcommand as defined by the 'expose()'
    decorator used on a Controller function.
    
    Keyword arguments:
    cmd_name --  The command name as store in the global 'namespaces'.  For
                 example, namespaces['root'].commands['cmd_name'].
                
    """
    log.debug("processing passed command '%s'", cmd_name)
    cmd_name = cmd_name.rstrip('*') # stripped off of namespace if passed
    if cmd_name in namespaces.keys():
        namespace = cmd_name
    else:
        namespace = 'root'
    
    # Handle hidden -help commands
    m = re.match('(.*)-help', cmd_name)
    if m and m.group(1) in namespaces.keys():   
        namespace = m.group(1)
        raise CementArgumentError, \
            "'%s' is a namespace*, not a command.  See '%s --help' instead." % \
                (namespace, namespace)
        
    # Parse cli options and arguments
    (cli_opts, cli_args) = parse_options(namespace=namespace)
    if namespace == 'root':
        set_config_opts_per_cli_opts('root', cli_opts)
    else:
        # If it merges in root ooptions, then it overrites them too.
        if  namespaces[namespace].config.has_key('merge_root_options') and \
            namespaces[namespace].config['merge_root_options']:
            set_config_opts_per_cli_opts('root', cli_opts)    
        set_config_opts_per_cli_opts(namespace, cli_opts)
    
    # Run all post options hooks
    for res in run_hooks('post_options_hook', cli_opts, cli_args):
        pass # Doesn't expect a result
    
    # If it isn't the root namespace, then the first arg is the namespace
    # and the second is the actual command.
    if namespace == 'root':
        actual_cmd = cmd_name
    else:
        try:
            actual_cmd = cli_args[1]
        except IndexError:
            raise CementArgumentError, "%s is a namespace* which requires a sub-command.  See '%s --help?" % (namespace, namespace)
    
    # Jsonify it... json commands are hidden
    if cli_opts.enable_json:
        actual_cmd = "%s-json" % actual_cmd
        
    if namespaces[namespace].commands.has_key(actual_cmd):
        cmd = namespaces[namespace].commands[actual_cmd]
        log.debug("executing command '%s'" % actual_cmd)
        
        # Import the command module
        #mod = __import__(cmd['module'], globals(), locals(), [cmd['controller']], -1)
        
        # Import the controller from the module
        #controller = getattr(mod, cmd['controller'])()
        
        # Run the command function
        #func = getattr(controller, cmd['func'])(cli_opts, cli_args)
        controller = namespaces[cmd['controller_namespace']].controller()
        func = getattr(controller, cmd['func'])(cli_opts, cli_args)


        
    else:
        raise CementArgumentError, "Unknown command '%s', see --help?" % actual_cmd
        