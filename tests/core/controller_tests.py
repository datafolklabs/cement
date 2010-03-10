
import os
import shutil
from tempfile import mkdtemp
from configobj import ConfigObj
from nose.tools import with_setup, raises, ok_

from cement.core.exc import CementRuntimeError, CementConfigError
from cement.core.controller import CementController

tmpdir = None

def setup_func():
    "set up test fixtures"
    global tmpdir
    tmpdir = mkdtemp()
    
def teardown_func():
    "tear down test fixtures"
    global tmpdir
    shutil.rmtree(tmpdir)

@with_setup(setup_func, teardown_func)
def test_controller_class():
    # FIXME: passing bogus cause cli_opts is actually an object, but we just
    # want to test that self.cli_opts is getting assigned
    c = CementController(cli_opts='bogus', cli_args=['a', 'b'])
    assert c.cli_opts == 'bogus', "self.cli_opts is not getting set."
    assert 'a' in c.cli_args, "self.cli_opts is not getting set."
    
# FIX ME: rest of stuff requires a running/installed cement app    