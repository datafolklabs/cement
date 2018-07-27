
import os
import shutil
import pytest
from cement.utils.misc import rando as _rando
from tempfile import mkstemp, mkdtemp


@pytest.fixture(scope="function")
def tmp(request):
    class Tmp(object):
        cleanup = True

        def __init__(self):
            self.dir = mkdtemp()
            _, self.file = mkstemp(dir=self.dir)
    t = Tmp()
    yield t

    # cleanup
    if os.path.exists(t.dir) and t.cleanup is True:
        shutil.rmtree(t.dir)


@pytest.fixture(scope="function")
def key(request):
    yield _rando()


@pytest.fixture(scope="function")
def rando(request):
    yield _rando()
