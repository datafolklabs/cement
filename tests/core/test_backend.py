
from cement.core import backend

def test_version():
    ### ensure that we bump things properly on version changes
    assert backend.VERSION[0] == 2
    assert backend.VERSION[1] == 99
    assert backend.VERSION[2] == 1
    assert backend.VERSION[3] == 'alpha'
    assert backend.VERSION[4] == 0
