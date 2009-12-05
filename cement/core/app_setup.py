
from pkg_resources import get_distribution

from cement.core.log import setup_logging
from cement.core.options import init_parser, parse_options
from cement.core.config import set_config_opts_per_file
from cement.core.options import set_config_opts_per_cli_opts

def lay_cement(config, version_banner=None):
    if not version_banner:
        version_banner = get_distribution(config['app_module']).version
        
    config = set_config_opts_per_file(config, config['app_module'], 
                                      config['config_file'])
    options = init_parser(config, version_banner)
    (config, cli_opts, cli_args) = parse_options(config, options)
    config = set_config_opts_per_cli_opts(config, cli_opts)
    setup_logging(config)
    return (config, cli_opts, cli_args)