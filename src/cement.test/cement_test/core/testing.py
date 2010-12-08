
import os
import shutil
from tempfile import mkdtemp
from cement import namespaces

def setup_func():
    """Setup operations before every test."""
    namespaces['root'].config['datadir'] = mkdtemp()
    if not os.path.exists(namespaces['root'].config['datadir']):
        os.makedirs(namespaces['root'].config['datadir'])

def teardown_func():
    """Teardown operations after every test."""
    if os.path.exists(namespaces['root'].config['datadir']):
        shutil.rmtree(namespaces['root'].config['datadir'])