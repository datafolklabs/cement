"""
Cement core interface module.

"""

import sys
from ..core import exc
from ..utils.misc import _inspect_app

DEFAULT_META = ['interface', 'label', 'config_defaults', 'config_section']


class Interface(object):

    """
    An interface definition class.  All Interfaces should subclass from
    here.  Note that this is not an implementation and should never be
    used directly.
    """

    def __init__(self):
        raise exc.InterfaceError("Interfaces can not be used directly.")


class Attribute(object):

    """
    An interface attribute definition.

    :param description: The description of the attribute.

    """

    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return "<interface.Attribute - '%s'>" % self.description


def validate(interface, obj, members=None, meta=DEFAULT_META):
    """
    A wrapper to validate interfaces.

    :param interface: The interface class to validate against
    :param obj: The object to validate.
    :param members: The object members that must exist.
    :param meta: The meta object members that must exist.
    :raises: cement.core.exc.InterfaceError

    """
    if members is None:
        members = []
    invalid = []

    if hasattr(obj, '_meta') and interface != obj._meta.interface:
        raise exc.InterfaceError("%s does not implement %s." %
                                 (obj, interface))

    for member in members:
        if not hasattr(obj, member):
            invalid.append(member)

    if not hasattr(obj, '_meta'):
        invalid.append("_meta")
    else:
        for member in meta:
            if not hasattr(obj._meta, member):
                invalid.append("_meta.%s" % member)

    if invalid:
        raise exc.InterfaceError("Invalid or missing: %s in %s" %
                                 (invalid, obj))


# Backwards compatibility
def list():
    # TODO: deprecation warning
    app = _inspect_app(sys._getframe(1))
    return __builtins__['list'](app.handlers._handlers.keys())
