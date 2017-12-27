
import os
import shutil
import pytest
from tempfile import mkstemp, mkdtemp

@pytest.fixture(scope="function")
def tmp(request):
    class Tmp(object):
        def __init__(self):
            self.dir = mkdtemp()
            _, self.file = mkstemp(dir=self.dir)
    t = Tmp()
    yield t

    # cleanup
    if os.path.exists(t.dir):
        shutil.rmtree(t.dir)
