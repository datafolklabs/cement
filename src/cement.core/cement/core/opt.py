"""Cement methods and classes to handle cli option/arg parsing."""

import os
import sys
import re
from optparse import OptionParser, IndentedHelpFormatter, OptionConflictError

from cement import namespaces
from cement.core.log import get_logger
            
log = get_logger(__name__)            
        

def init_parser(banner=None):
    """
    Create an OptionParser object and returns its parser member.
    
    Keyword arguments:
    
        banner
            Optional version banner to display for --version
    
    Returns: OptionParser object.
    
    """
    fmt = IndentedHelpFormatter(
            indent_increment=4, max_help_position=32, width=77, short_first=1
            )
    parser = OptionParser(formatter=fmt, version=banner)
    return parser

    
def parse_options(namespace='root', ignore_conflicts=False): 
    """
    The actual method that parses the command line options and args.  Also
    handles all the magic that happens when you pass --help to your app.  It
    also handles merging root options into plugins, if the plugins config
    is set to do so (merge_root_options)
    
    Required Arguments:
    
        namespace
            The namespace to parse options for (defaullt: 'root')
    
    Returns: tuple (options, args)
    
    """

    # FIX ME: This method is very messy/confusing.
    
    log.debug("parsing command line opts/args for '%s' namespace" % namespace)
    if namespace != 'root':
        if namespaces[namespace].config.has_key('merge_root_options') and \
           namespaces[namespace].config['merge_root_options']:
            for opt in namespaces['root'].options._get_all_options(): 
                if opt.get_opt_string() == '--help':
                    pass
                elif opt.get_opt_string() == '--version':
                    pass
                else:
                    try:
                        namespaces[namespace].options.add_option(opt)
                    except OptionConflictError, error:
                        if not ignore_conflicts:
                            raise OptionConflictError, error
    
    cmd_txt = ''
    line = '    '
    if namespaces[namespace].commands:
        for cmd in namespaces[namespace].commands:    
            cmd_with_dashes = re.sub('_', '-', cmd)
            if namespaces[namespace].commands[cmd]['is_hidden']:
                pass
            else:
                if line == '    ':
                    line += '%s' % cmd_with_dashes
                elif len(line) + len(cmd_with_dashes) < 75:
                    line += ', %s' % cmd_with_dashes
                else:
                    cmd_txt += "%s \n" % line
                    line = '    %s' % cmd_with_dashes
    if line != '    ':
        cmd_txt += "%s\n" % line
        
    # Do the same thing, but with namespaces (if applicable to each namespace)
    nam_txt = ''
    line = '    '
    script = os.path.basename(sys.argv[0])
    if namespace == 'root':
        for nam in namespaces: 
            nam_with_dashes = re.sub('_', '-', nam)
            if nam != 'root' and namespaces[nam].commands:
                if namespaces[nam].is_hidden:
                    pass
                else:
                    # dirty, but have to account for namespaces with only 
                    # hidden commands... which we don't want to show
                    show_namespace = False
                    for cmd in namespaces[nam].commands:
                        if not namespaces[nam].commands[cmd]['is_hidden']:
                            show_namespace = True
                            break

                    if show_namespace:       
                        if line == '    ':
                            line += '%s' % nam_with_dashes
                        elif len(line) + len(nam_with_dashes) < 75:
                            line += ', %s' % nam_with_dashes
                        else:
                            nam_txt += "%s \n" % line
                            line = '    %s' % nam_with_dashes
                            
        if line != '    ':
            nam_txt += "%s\n" % line    
    
        if nam_txt == "":
            namespaces[namespace].options.usage = """  %s <COMMAND> [ARGS] --(OPTIONS)

Commands:  
%s
Help?  try '[COMMAND]-help' OR '[NAMESPACE] --help'""" % \
            (script, cmd_txt)

        else:
            namespaces[namespace].options.usage = """  %s <COMMAND> [ARGS] --(OPTIONS)

Commands:  
%s
Namespaces (Nested SubCommands):
%s
Help?  try '[COMMAND]-help' OR '[NAMESPACE] --help'""" % \
        (script, cmd_txt, nam_txt)
                         
    else: # namespace not root
        namespaces[namespace].options.usage = """  %s %s <SUBCOMMAND> [ARGS] --(OPTIONS)

Sub-Commands:  
%s
Help?  try '[SUBCOMMAND]-help'""" % \
        (script, re.sub('_', '-', namespace), cmd_txt)
        

    (opts, args) = namespaces[namespace].options.parse_args()
    
    return (opts, args)

