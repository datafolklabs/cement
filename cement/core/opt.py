"""Cement methods and classes to handle cli option/arg parsing."""

import sys, os
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
                    except OptionConflictError, e:
                        if not ignore_conflicts:
                            raise OptionConflictError, e
    
    cmd_txt = ''
    line = '    '
    if namespaces[namespace].commands:
        for c in namespaces[namespace].commands:    
            if c.endswith('-help') or namespaces[namespace].commands[c]['is_hidden']:
                pass
            else:
                if line == '    ':
                    line += '%s' % c
                elif len(line) + len(c) < 75:
                    line += ', %s' % c
                else:
                    cmd_txt += "%s \n" % line
                    line = '    %s' % c

    # Determine whether to display namespaces
    if namespace == 'root':
        for nam in namespaces: 
            if nam != 'root' and namespaces[nam].commands:
                if namespaces[nam].is_hidden:
                    pass
                else:
                    # dirty, but have to account for namespaces with only 
                    # hidden commands... which we don't want to show
                    show_namespace = False
                    for c in namespaces[nam].commands:
                        if not namespaces[nam].commands[c]['is_hidden']:
                            show_namespace = True
                            break

                    if show_namespace:       
                        if line == '    ':
                            line += '%s*' % nam
                        elif len(line) + len(nam) < 75:
                            line += ', %s*' % nam
                        else:
                            cmd_txt += "%s \n" % line
                            line = '    %s*' % nam

    if line != '    ':
        cmd_txt += "%s\n" % line
    
    if namespace != 'root':
        namespace_txt = ' %s' % namespace
        cmd_type_txt = 'SUBCOMMAND'
    else:
        namespace_txt = ''
        cmd_type_txt = 'COMMAND'
    
    script = os.path.basename(sys.argv[0])
    namespaces[namespace].options.usage = """  %s%s [%s] --(OPTIONS)

Commands:  
%s
    
Help?  try [%s]-help""" % (script, namespace_txt, cmd_type_txt, cmd_txt, 
                           cmd_type_txt)

    (opts, args) = namespaces[namespace].options.parse_args()
    
    return (opts, args)

