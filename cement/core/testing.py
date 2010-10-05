"""Helper functions for testing applications built on Cement."""

import sys
from cement import namespaces
from cement.core.controller import run_controller_command
from cement.core.opt import parse_options

def simulate():
    """
    Simulate running a command at command line.  Requires sys.argv to have
    the exact args set to it as would be passed at command line.
    
    Usage:
    
    .. code-block:: python
    
        import sys
        from cement.core.testing import simulate
        
        sys.argv = ['helloworld', 'example', 'cmd1', '--test-option']
        res = simulate()
        
    """
    if sys.argv[1] in namespaces:
        (opts, args) = parse_options(sys.argv[1], ignore_conflicts=True)
        res = run_controller_command(sys.argv[1], sys.argv[2], opts, args) 
    else:
        (opts, args) = parse_options('root', ignore_conflicts=True)
        res = run_controller_command('root', sys.argv[1], opts, args) 
    return res