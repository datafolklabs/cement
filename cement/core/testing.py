"""Helper functions for testing applications built on Cement."""

import os
import sys
import re
from shutil import rmtree
from tempfile import mkdtemp

from cement import namespaces
from cement.core.namespace import get_config
from cement.core.exc import CementRuntimeError
from cement.core.controller import run_controller_command
from cement.core.command import run_command
from cement.core.opt import parse_options

def simulate(args=[]):
    """
    Simulate running a command at command line.  Requires args to have
    the exact args set to it as would be passed at command line.
    
    Required arguments:
    
        args
            The args to pass to sys.argv
            
    Usage:
    
    .. code-block:: python
    
        import sys
        from cement.core.testing import simulate
        
        args = ['helloworld', 'example', 'cmd1', '--test-option']
        res = simulate(args)
        
    """
    if not len(sys.argv) >= 1:
        raise CementRuntimeError, "args must be set properly."
        
    sys.argv = args
    
    #namespace = 'root' # default
    #controller_namespace = 'root' # default
    #    
    #if sys.argv[1] in namespaces:
    #    namespace = sys.argv[1]
    #    
    #for nam in namespaces:
    #    if sys.argv[1] in namespaces[nam].commands:
    #        controller_namespace = namespaces[nam].commands[sys.argv[1]]['controller_namespace']
    #        break 
    
    # get the command to run
    #if namespace == 'root':
    #    cmd = sys.argv[1]
    #else:
    #    if not len(sys.argv) >= 3:
    #        raise CementRuntimeError, "A subcommand (additional arg) is required."
    #    else:
    #        cmd = sys.argv[2]

    # unconvert dashes
    #cmd = re.sub('-', '_', cmd)
    #
    #print controller_namespace
    #print namespace
    #print cmd
    
    #(opts, args) = parse_options(controller_namespace, ignore_conflicts=True)
    #(res_dict, output_txt) = run_controller_command(controller_namespace, cmd, opts, args) 
    (res_dict, output_txt) = run_command(cmd_name=sys.argv[1], ignore_conflicts=True)
    return (res_dict, output_txt)
