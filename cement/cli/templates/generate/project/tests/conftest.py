"""
PyTest Fixtures.
"""

from collections.abc import Generator

import pytest
from cement import fs


@pytest.fixture(scope="function")
def tmp(request: pytest.FixtureRequest) -> Generator[fs.Tmp, None, None]:
    """
    Create a `tmp` object that geneates a unique temporary directory, and file
    for each test function that requires it.
    """
    t = fs.Tmp()
    yield t
    t.remove()
