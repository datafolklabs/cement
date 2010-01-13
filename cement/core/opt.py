"""Cement methods and classes to handle cli option/arg parsing."""

import sys, os
from optparse import OptionParser, IndentedHelpFormatter

from cement import namespaces

            
class Options(object):
    """
    This class is used to setup the OptParse object for later use, and is
    the object that is passed around thoughout the application.
    """
    def __init__(self):
        self.parser = None
        self.init_parser()
        
    def add_default_options(self):
        """
        Sets up default options for applications using Cement.
        """
        pass  
         
    def init_parser(self, version_banner=None):
        """
        Sets up the Options object and returns it for use throughout the 
        application.
    
        Arguments
    
        version_banner => option txt to be display for --version.
        """
        fmt = IndentedHelpFormatter(
            indent_increment=4, max_help_position=32, width=77, short_first=1
            )
        self.parser = OptionParser(formatter=fmt, version=version_banner)
    
def get_options():
    o = Options()
    return o
    

def init_parser(version_banner=None):
    fmt = IndentedHelpFormatter(
            indent_increment=4, max_help_position=32, width=77, short_first=1
            )
    parser = OptionParser(formatter=fmt, version=version_banner)
    return parser

    
def parse_options(namespace='global'): 
    """
    The actual method that parses the command line options and args.  
    
    Arguments:
    
    config => dict containing the application configurations.
    options_obj => The options object used to pass the parser around.
    commands => Plugin commands to be added to the --help output.
    
    Returns => a tuple of (options, args)
    """
    global namespaces

    if namespaces[namespace].config.has_key('merge_global_options') and \
       namespaces[namespace].config['merge_global_options']:
        for opt in namespaces['global'].options._get_all_options(): 
            if opt.get_opt_string() == '--help':
                pass
            elif opt.get_opt_string() == '--version':
                pass
            else:
                namespaces[namespace].options.add_option(opt)
    
    cmd_txt = ''
    line = '    '
    if namespaces[namespace].commands:
        for c in namespaces[namespace].commands:    
            if c.endswith('-help') or namespaces[namespace].commands[c].is_hidden:
                pass
            else:
                if line == '    ':
                    line += '%s' % c
                elif len(line) + len(c) < 75:
                    line += ', %s' % c
                else:
                    cmd_txt += "%s \n" % line
                    line = '    %s' % c

    # determine whether to display namespaces
    if namespace == 'global':
        for nam in namespaces: 
            if nam != 'global' and namespaces[nam].commands:
                if namespaces[nam].is_hidden:
                    pass
                else:
                    # dirty, but have to account for namespaces with only 
                    # hidden commands... which we don't want to show
                    show_namespace = False
                    for c in namespaces[nam].commands:
                        if not namespaces[nam].commands[c].is_hidden:
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
    
    if namespace != 'global':
        namespace_txt = ' %s' % namespace
        cmd_type_txt = 'SUBCOMMAND'
    else:
        namespace_txt = ''
        cmd_type_txt = 'COMMAND'
    
    script = os.path.basename(sys.argv[0])
    namespaces[namespace].options.usage = """  %s%s [%s] --(OPTIONS)

Commands:  
%s
    
Help?  try [%s]-help""" % (script, namespace_txt, cmd_type_txt, cmd_txt, cmd_type_txt)

    (opts, args) = namespaces[namespace].options.parse_args()
    
    return (opts, args)

