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
    if sys.argv[1] in namespaces:
        if not len(sys.argv) >= 3:
            raise CementRuntimeError, "A subcommand (additional arg) is required."
        else:
            namespace = sys.argv[1]
            cmd = sys.argv[2]
    else:
        namespace = 'root'
        cmd = sys.argv[1]
        
    cmd = re.sub('-', '_', cmd)
    
    (opts, args) = parse_options(namespace, ignore_conflicts=True)
    (res_dict, output_txt) = run_controller_command(namespace, cmd, opts, args) 
    return (res_dict, output_txt)
