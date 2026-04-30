
import os
import shutil

import pytest

from cement.utils import fs
from cement.utils.misc import rando as _rando


@pytest.fixture
def tmp(request):
    t = fs.Tmp()
    yield t

    # cleanup
    if os.path.exists(t.dir) and t.cleanup is True:
        shutil.rmtree(t.dir)


@pytest.fixture
def key(request):
    return _rando()


@pytest.fixture
def rando(request):
    return _rando()[:12]
