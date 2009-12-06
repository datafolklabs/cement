"""Cement methods and classes to handle cli option/arg parsing."""

from optparse import OptionParser, IndentedHelpFormatter

class Options(object):
    """
    This class is used to setup the OptParse object for later use, and is
    the object that is passed around thoughout the application.
    """
    def __init__(self, config, version_banner):
        self.config = config
        fmt = IndentedHelpFormatter(
            indent_increment=4, max_help_position=32, width=77, short_first=1
            )
        self.parser = OptionParser(
            version=version_banner, formatter=fmt
            )
            
    def add_default_options(self):
        """
        Sets up default options for applications using Cement.
        """
        self.parser.add_option('-D', '--debug', action ='store_true', 
            dest='debug', default=None, help='debug output'
            ) 
    
            
def init_parser(config, version_banner=None):
    """
    Sets up the Options object and returns it for use throughout the 
    application.
    
    Arguments
    
    config => dict containing the application configurations
    version_banner => option txt to be display for --version.
    """
    o = Options(config, version_banner)
    return o
    
    
def parse_options(config, options_obj, commands=None): 
    """
    The actual method that parses the command line options and args.  
    
    Arguments:
    
    config => dict containing the application configurations.
    options_obj => The options object used to pass the parser around.
    commands => Plugin commands to be added to the --help output.
    
    Returns => a tuple of (config, options, args)
    """
    o = options_obj
    
    cmd_txt = ''
    line = ''
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
    
    Returns the updated config dict.
    """
    for opt in config:
        try:
            val = getattr(cli_opts, opt)
            if val:
                config[opt] = val
        except AttributeError:
            pass
    return config