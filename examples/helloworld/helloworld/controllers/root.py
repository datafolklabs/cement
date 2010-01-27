"""
This is the RootController for the helloworld application.  Usually this
file will remain pretty sparse, however it is a good place for miscellaneous
commands that might night need there own namespace or controller.  
"""

from cement.core.controller import CementController, expose

class RootController(CementController):
    @expose('helloworld.templates.error', is_hidden=True)
    def error(self, errors={}):
        return dict(errors=errors)