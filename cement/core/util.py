    
import sys
    
from cement import namespaces
from cement.core.controller import run_controller_command

def abort(errors):
    """
    Quick way of aborting a controller command function on errors.  Used as 
    an alternative to simply raising an exception.  Calls the applications
    RootController().error command function which inturn renders the error
    output via Genshi template.
    
    Required Arguments:
    
        errors
            A dictionary of errors.
    
    Exits with a code of '1'.
    
    
    Usage:
    
    .. code-block:: python
    
        from cement.core.controller import CementController, expose
        from cement.core.util import abort
        
        class MyController(CementController):
            @expose('myapp.templates.namespace.mycmd')
            def mycmd(self, cli_opts, cli_args):
                errors = {}
                
                if something:
                    errors['MyErrorDef'] = "Something didn't work out"
                if something_else:
                    errors['MyErrorDef'] = "Something else didn't work out"
                
                if errors:
                    abort(errors)        
                ...
            
    """
    if namespaces['root'].config['output_engine'] == 'json':
        run_controller_command('root', 'error_json', errors=errors)
    else:
        run_controller_command('root', 'error', errors=errors)
    sys.exit(1)
    