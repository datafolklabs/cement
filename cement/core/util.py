    
import sys
    
from cement import namespaces
from cement.core.controller import run_controller_command

def abort(errors):
    if namespaces['root'].config['output_engine'] == 'json':
        run_controller_command('root', 'error_json', errors=errors)
    else:
        run_controller_command('root', 'error', errors=errors)
    sys.exit(1)
    