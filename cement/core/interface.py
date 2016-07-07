"""
Cement core interface module.

"""

from ..core import exc, backend

DEFAULT_META = ['interface', 'label', 'config_defaults', 'config_section']


def list():
    """
    DEPRECATION WARNING: This function is deprecated as of Cement 2.9
    in favor of the `CementApp.handler.list_types()` function, and will be
    removed in future versions of Cement.

    Return a list of defined interfaces (handler types).

    :returns: List of defined interfaces
    :rtype: ``list``

    """

    # FIXME: Can't print a deprecation warning here because we don't have
    # access to the app... and this is too deep to use minimal logger... ;\

    return backend.__handlers__.keys()


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


def validate(interface, obj, members=[], meta=DEFAULT_META):
    """
    A wrapper to validate interfaces.

    :param interface: The interface class to validate against
    :param obj: The object to validate.
    :param members: The object members that must exist.
    :param meta: The meta object members that must exist.
    :raises: cement.core.exc.InterfaceError

    """
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
