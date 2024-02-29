
import os
import shutil
import pytest
from cement.utils.misc import rando as _rando
from cement.utils import fs


@pytest.fixture(scope="function")
def tmp(request):
    t = fs.Tmp()
    yield t

    # cleanup
    if os.path.exists(t.dir) and t.cleanup is True:
        shutil.rmtree(t.dir)


@pytest.fixture(scope="function")
def key(request):
    yield _rando()


@pytest.fixture(scope="function")
def rando(request):
    yield _rando()[:12]
