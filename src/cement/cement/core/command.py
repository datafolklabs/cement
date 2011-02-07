"""These methods and classes controller how commands are parsed and run."""

import re

from cement import namespaces
from cement.core.log import get_logger
from cement.core.hook import run_hooks
from cement.core.opt import parse_options
from cement.core.controller import run_controller_command
from cement.core.exc import CementArgumentError

log = get_logger(__name__)
        
def run_command(cmd_name=None, ignore_conflicts=False):
    """
    Run the command or namespace-subcommand as defined by the 'expose()'
    decorator used on a Controller function.
    
    Keyword arguments:
    
        cmd_name
            The command name as store in the global 'namespaces'. For 
            example, namespaces['root'].commands['cmd_name'].
                
    """
    log.debug("processing passed command '%s'", cmd_name)
    
    # bit of a hack... but if cmd_name starts with - then no command passed
    if cmd_name.startswith('-'):
        cmd_name = 'default'
        
    orig_cmd = cmd_name
    cmd_name = re.sub('-', '_', cmd_name)
    
    if cmd_name in namespaces.keys():
        namespace = cmd_name
    else:
        namespace = 'root'
                               
    # Parse cli options and arguments
    (cli_opts, cli_args) = parse_options(namespace=namespace, 
                                         ignore_conflicts=ignore_conflicts)

    # Run all post options hooks
    for res in run_hooks('post_options_hook', cli_opts, cli_args):
        pass # Doesn't expect a result
    
    # If it isn't the root namespace, then the first arg is the namespace
    # and the second is the actual command.
    if namespace == 'root':
        actual_cmd = cmd_name
    else:
        try:
            actual_cmd = re.sub('-', '_', cli_args[1])
        except IndexError:
            if namespaces[namespace].commands.has_key('default'):
                actual_cmd = 'default'
            else:
                raise CementArgumentError, \
                    "%s is a namespace* " % namespace + \
                    "which requires a sub-command.  See " + \
                    "'%s --help'" % namespace
    
    if namespaces[namespace].commands.has_key(actual_cmd):
        cmd = namespaces[namespace].commands[actual_cmd]
        log.debug("executing command '%s'" % actual_cmd)
        (res, out_txt) = run_controller_command(cmd['controller_namespace'], 
                                                cmd['func'], 
                                                cli_opts, cli_args)  
        return (res, out_txt)
    else:
        raise CementArgumentError, "Unknown command '%s', see --help?" % \
                                   actual_cmd
        
