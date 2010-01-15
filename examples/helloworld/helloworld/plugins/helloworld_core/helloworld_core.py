"""This is the core plugin for helloworld."""

import sys, os

from cement import namespaces
from cement.core.log import get_logger
from cement.core.opt import init_parser
from cement.core.hook import define_hook, register_hook
from cement.core.command import CementCommand, register_command
from cement.core.plugin import CementPlugin, register_plugin

log = get_logger(__name__)

VERSION = '0.1'
REQUIRED_CEMENT_API = '20091211'

# Optional: Allows you to customize the output of --version
BANNER = """
helloworld.plugins.helloworld_core v%s 
""" % (VERSION)
        
@register_plugin() 
class helloworldPlugin(CementPlugin):
    def __init__(self):
        CementPlugin.__init__(self,
            label = 'helloworld',
            version = VERSION,
            description = 'Core plugin for helloworld',
            required_api = REQUIRED_CEMENT_API,
            version_banner = BANNER,
            )

