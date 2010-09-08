"""
This is the ExampleController for the cementtest application.  This can be used
to expose commands to the example namespace which will be accessible under:

    $ cementtest example --help
  
"""

import sys

from cement.core.namespace import get_config
from cement.core.log import get_logger
from cement.core.controller import CementController, expose
from cement.core.hook import run_hooks

from cementtest.model.example import ExampleModel

log = get_logger(__name__)

class ExampleController(CementController):
    @expose(namespace='example')
    def cmd1(self):
        foo='bar'
        print foo
        return dict(foo=foo)
        