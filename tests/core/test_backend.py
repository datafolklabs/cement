
from cement.core import backend


def test_version():
    # ensure that we bump things properly on version changes
    assert backend.VERSION[0] == 3
    assert backend.VERSION[1] == 0
    assert backend.VERSION[2] == 10
    assert backend.VERSION[3] == 'final'
    assert backend.VERSION[4] == 0
