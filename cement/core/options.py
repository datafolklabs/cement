#!/usr/bin/env python
#
# This file is a part of the Cement package.  Please see the
# README and LICENSE files includes with this software.
#

import sys,os
from cement import helpers as _h
from optparse import OptionParser, IndentedHelpFormatter

class Options(object):
    def __init__(self, config, ver_banner):
        self.config = config
        fmt = IndentedHelpFormatter(
            indent_increment=4,max_help_position=32, width=80, short_first=1
            )
        self.parser = OptionParser(
            version=ver_banner(), formatter=fmt
            )
            
    def add_default_options(self):
        self.parser.add_option('-D', '--debug', action ='store_true', 
            dest='debug', default=None, help='debug output'
            ) 
            
def init_parser(config, ver_banner):
    o = Options(config, ver_banner)
    return o
    
def parse_options(config, options_obj, commands): 
    o = options_obj
    
    cmd_txt = ''
    line = ''
    sorted_commands = h.sort_dict(commands)
    for c in commands:    
        if not c.endswith('-help'):
            if len(line) + len(c) < 55:
                line += '%s, ' % c
            else:
                cmd_txt += "%s \n" % line
                line = '           '

    if line != '           ':
        cmd_txt += "%s \n" % line
    cmd_txt = cmd_txt.strip(', ')
    
    o.parser.usage = """  %s [COMMAND] --(OPTIONS)

Commands:  getconfig, %s
    
Help?  try [COMMAND]-help""" % (config['app_name'], cmd_txt)

    o.add_default_options()
    (opts, args) = o.parser.parse_args()
    
    if opts.debug:
        config['debug'] = opts.debug
    return (config, opts, args)
    
    
def set_config_opts_per_file(config_opts, section, file):
    """
    Parse config file options for config_opts.  Will do nothing if the config 
    file does not exist.
    """
    log.debug('set_config_opts_per_file()')
    if not config_opts.has_key('config_source'):
        config_opts['config_source'] = []
        
    if os.path.exists(file):
        config_opts['config_source'].append(file)
        config_opts['config_file'] = file
        config = ConfigObj(file)
        try:
            config_opts.update(config[section])
        except KeyError, e:
            raise CementConfigError, \
                'missing section %s in %s.  ignoring config...' % (section, file)

        for option in config[section]:
            if config[section][option] in ['True', 'true', True]:
                config_opts[option] = True
            elif config[section][option] in ['False', 'false', False]:
                config_opts[option] = False

    return config_opts