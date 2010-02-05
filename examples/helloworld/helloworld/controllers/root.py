"""
This is the RootController for the helloworld application.  Usually this
file will remain pretty sparse, however it is a good place for miscellaneous
commands that might not need there own namespace or controller.  
"""

from cement.core.namespace import CementNamespace, register_namespace
from cement.core.controller import CementController, expose
from cement.core.hook import define_hook, run_hooks

# non-plugin namespaces
@register_namespace()
class GreetingNamespace(CementNamespace):
    def __init__(self):
        CementNamespace.__init__(self,
            label='greeting',
            required_api='0.5-0.6:20100115',
            controller = 'GreetingController'
            )



            
class RootController(CementController):
    @expose('helloworld.templates.root.error', is_hidden=True)
    def error(self, errors={}):
        return dict(errors=errors)
        
    @expose()
    def hook_example(self, cli_opts, cli_args):
        for res in run_hooks('my_example_hook'):
            pass