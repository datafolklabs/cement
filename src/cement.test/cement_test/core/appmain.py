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

from cement_test.core.config import default_config
from cement_test.core.exc import CementTestArgumentError, CementTestConfigError, \
                                 CementTestRuntimeError

VERSION = get_distribution('cement_test').version
BANNER = """
cement_test version %s
""" % VERSION

def main(args=None):
    try:    
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

    lay_cement(config=test_config, banner=BANNER, args=args)
    log = get_logger(__name__)
    log.debug("Cement Framework Initialized!")

    if not len(args) > 1:
        args.append('default')

    (res, output_txt) = run_command(args[1])
    return (res, output_txt)
    
if __name__ == '__main__':
    main()
    
