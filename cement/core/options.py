#!/usr/bin/env python
#
# This file is a part of the Cement package.  Please see the
# README and LICENSE files includes with this software.
#

import sys,os
from cement import helpers as _h
from cement.helpers.misc import sort_dict
from optparse import OptionParser, IndentedHelpFormatter

class Options(object):
    def __init__(self, config, version_banner):
        self.config = config
        fmt = IndentedHelpFormatter(
            indent_increment=4,max_help_position=32, width=80, short_first=1
            )
        self.parser = OptionParser(
            version=version_banner, formatter=fmt
            )
            
    def add_default_options(self):
        self.parser.add_option('-D', '--debug', action ='store_true', 
            dest='debug', default=None, help='debug output'
            ) 
            
def init_parser(config, ver_banner):
    o = Options(config, ver_banner)
    return o
    
def parse_options(config, options_obj, commands=None): 
    o = options_obj
    
    cmd_txt = ''
    line = ''
    sorted_commands = sort_dict(commands)
    if commands:
        for c in commands:    
            if not c.endswith('-help'):
                if len(line) + len(c) < 55:
                    line += '%s  ' % c
                else:
                    cmd_txt += "%s  \n" % line
                    line = '           '

    if line != '           ':
        cmd_txt += "%s  \n" % line
    
    o.parser.usage = """  %s [COMMAND] --(OPTIONS)

Commands:  
    getconfig  %s
    
Help?  try [COMMAND]-help""" % (config['app_name'], cmd_txt)

    o.add_default_options()
    (opts, args) = o.parser.parse_args()
    
    return (config, opts, args)
    
    
def set_config_opts_per_cli_opts(config, cli_opts):
    """
    Determine if any config optons were passed via cli options, and if so
    override the config option.
    """
    for opt in config:
        try:
            val = getattr(cli_opts, opt)
            if val:
                config[opt] = val
        except AttributeError, e:
            pass
    return config