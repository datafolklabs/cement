
import os
import shutil
from tempfile import mkdtemp
from configobj import ConfigObj
from nose.tools import with_setup, raises, ok_

from cement.core.exc import CementRuntimeError, CementConfigError
from cement.core.configuration import ensure_api_compat, CEMENT_API, t_f_pass
from cement.core.configuration import validate_config

tmpdir = None

def setup_func():
    "set up test fixtures"
    global tmpdir
    tmpdir = mkdtemp()
    
def teardown_func():
    "tear down test fixtures"
    global tmpdir
    shutil.rmtree(tmpdir)

@raises(CementRuntimeError)
@with_setup(setup_func, teardown_func)
def test_ensure_api_compat_bad():
    ensure_api_compat(__name__, 'xxxxx')

@with_setup(setup_func, teardown_func)
def test_ensure_api_compat():
    ok_(ensure_api_compat(__name__, CEMENT_API))

@with_setup(setup_func, teardown_func)
def test_validate_config():
    global tmpdir
    prefix = tmpdir
    
    dcf = ConfigObj() # default config
    dcf['config_source'] = ['defaults']
    dcf['app_name'] = 'helloworld' # name for cli like /etc/<app_name>
    dcf['app_egg_name'] = 'helloworld' # name from setup.py
    dcf['app_module'] = 'helloworld' # name of the library dir

    dcf['enabled_plugins'] = [] # no default plugins, add via the config file
    dcf['debug'] = False
    dcf['datadir'] = '%s/data' % prefix
    dcf['tmpdir'] = '%s/tmp' % prefix
    dcf['log_file'] = '%s/log/%s.log' % (prefix, dcf['app_name'])
    dcf['plugin_config_dir'] = '%s/etc/plugins.d' % prefix
    dcf['log_to_console'] = True
    dcf['output_engine'] = 'genshi'
    dcf['show_plugin_load'] = True

    # By default look in /etc and ~/ for config files.  You should probably
    # symlink /etc/<your_app> => ./etc/<your_app> for easy development.
    dcf['config_files'] = [
        os.path.join(prefix, 'etc', '%s.conf' % dcf['app_name']),
        ]
    
    validate_config(dcf)

@raises(CementConfigError)
@with_setup(setup_func, teardown_func)
def test_validate_config_bad():
    global tmpdir
    prefix = tmpdir
    
    dcf = ConfigObj() # default config    
    validate_config(dcf)

@with_setup(setup_func, teardown_func)
def test_t_f_pass():
    for val in ['true', 'True', True]:
        yield check_true, val

    for val in ['false', 'False', False]:
        yield check_false, val
    
    for val in ['a', 'Blah Hah', 100]:
        yield check_pass, val
        
def check_true(val):
    assert t_f_pass(val) == True

def check_false(val):
    assert t_f_pass(val) == False

def check_pass(val):
    assert t_f_pass(val) == val
    