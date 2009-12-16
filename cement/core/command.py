
import re

from cement import namespaces, hooks
from cement.core.opt import parse_options
from cement.core.hook import run_hooks
from cement.core.configuration import set_config_opts_per_cli_opts
from cement.core.exc import *

class CementCommand(object):
    def __init__(self, cli_opts=None, cli_args=None):
        self.is_hidden = False # whether to display in command list at all
        self.cli_opts = cli_opts
        self.cli_args = cli_args
    
    def help(self):
        """Display command help information."""
        print "No help information available."
    
    def run(self):
        """Run the command actions."""
        print "No actions have been defined for this command."

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
    
    command_name = command_name.rstrip('*') 
    if command_name in namespaces.keys():
        namespace = command_name
    else:
        namespace = 'global'
    
    commands = namespaces[namespace].commands
    m = re.match('(.*)-help', command_name)
    if m and m.group(1) in namespaces.keys():   
        namespace = m.group(1)
        raise CementArgumentError, \
            "'%s' is a namespace*, not a command.  See '%s --help' instead." % \
                (namespace, namespace)
        
    (cli_opts, cli_args) = parse_options(namespace=namespace)
    set_config_opts_per_cli_opts(namespace, cli_opts)
    
    # FIX ME: need a global_pre_command_hook here so that clibasic can
    # look for -C and if so, parse the passed config files into the dict.
    args = (cli_opts, cli_args)
    for res in run_hooks('post_options_hook', cli_opts, cli_args):
        pass # doesn't expect a result
    
    if namespace == 'global':
        actual_cmd = command_name
    else:
        try:
            actual_cmd = cli_args[1]
        except IndexError:
            raise CementArgumentError, \
                "%s is a namespace* which requires a sub-command.  See '%s --help?" % (namespace, namespace)
    
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