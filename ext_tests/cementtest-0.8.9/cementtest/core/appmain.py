"""
This is the application's core code.  Unless you know the "ins-and-outs" of
The Cement CLI Application Framework, you probably should not modify the 
main() function of this file.

"""

import sys
from pkg_resources import get_distribution

from cement.core.exc import CementArgumentError, CementConfigError, \
                            CementRuntimeError
from cement.core.log import get_logger
from cement.core.app_setup import lay_cement
from cement.core.configuration import ensure_api_compat
from cement.core.command import run_command

from cementtest.core.config import default_config
from cementtest.core.exc import CementTestArgumentError, CementTestConfigError, \
                                 CementTestRuntimeError

REQUIRED_CEMENT_API = '0.7-0.8:20100210'
VERSION = get_distribution('cementtest').version
BANNER = """
cementtest version %s, built on Cement (api:%s)
""" % (VERSION, REQUIRED_CEMENT_API)

def main(args=None):
    try:
        ensure_api_compat(__name__, REQUIRED_CEMENT_API)    
        lay_cement(config=default_config, banner=BANNER, args=args)
    
        log = get_logger(__name__)
        log.debug("Cement Framework Initialized!")

        if not len(sys.argv) > 1:
            sys.argv.append('default')
        
        run_command(sys.argv[1])
            
    except CementArgumentError, e:
        # Display the apps exception names instead for the Cement exceptions.
        print("CementTestArgumentError > %s" % e)
        sys.exit(e.code)
    except CementConfigError, e:
        print("CementTestConfigError > %s" % e)
        sys.exit(e.code)
    except CementRuntimeError, e:
        print("CementTestRuntimeError > %s" % e)
        sys.exit(e.code)
    except CementTestArgumentError, e:
        print("CementTestArgumentError > %s" % e)
        sys.exit(e.code)
    except CementTestConfigError, e:
        print("CementTestConfigError > %s" % e)
        sys.exit(e.code)
    except CementTestRuntimeError, e:
        print("CementTestRuntimeError > %s" % e)
        sys.exit(e.code)
    sys.exit(0)

def nose_main(args, test_config):
    """
    This function provides an alternative to main() that is more friendly for 
    nose tests as it doesn't catch any exceptions.
    """

    ensure_api_compat(__name__, REQUIRED_CEMENT_API)    
    lay_cement(config=test_config, banner=BANNER, args=args)
    
    log = get_logger(__name__)
    log.debug("Cement Framework Initialized!")

    if not len(args) > 1:
        args.append('default')

    run_command(args[1])
    
if __name__ == '__main__':
    main()
    
