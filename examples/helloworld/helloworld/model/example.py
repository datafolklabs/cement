"""
This is an example model.  This can be anything, just a straight class
or perhaps an SQLAlchemy DeclarativeBase, etc.
"""

from cement.core.log import get_logger

log = get_logger(__name__)

class ExampleModel(object):
    id = int()
    label = u''
    description = u''