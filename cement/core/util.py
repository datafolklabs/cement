    
import sys
    
from cement import namespaces

def abort(errors):
    namespaces['global'].commands['error']['func'](errors)
    sys.exit(1)
    