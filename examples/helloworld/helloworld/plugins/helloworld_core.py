"""This is the core plugin for helloworld."""

import sys, os
from pkg_resources import get_distribution

from cement import namespaces
from cement.core.log import get_logger
from cement.core.opt import init_parser
from cement.core.hook import define_hook, register_hook
from cement.core.plugin import CementPlugin, register_plugin

from helloworld.appmain import VERSION, BANNER

log = get_logger(__name__)

REQUIRED_CEMENT_API = '0.5-0.6:20100115'
        
@register_plugin() 
class helloworldPlugin(CementPlugin):
    # define_hook('myfunction_hook')
    
    def __init__(self):
        CementPlugin.__init__(self,
            label='helloworld',
            version=VERSION,
            description='Core plugin for helloworld',
            required_api=REQUIRED_CEMENT_API,
            banner=BANNER,
            is_hidden=True,
            )

