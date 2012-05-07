"""
Cement core interface module.

"""

from ..core import exc

class Interface(object):
    def __init__(self):
        """
        An interface definition class.  All Interfaces should subclass from
        here.  Note that this is not an implementation and should never be
        used directly.
        """
        raise exc.CementInterfaceError("Interfaces can not be used directly.")
            
class Attribute(object):
    def __init__(self, description):
        """
        An interface attribute definition.
        
        Required Arguments:
        
            description
                The description of the attribute.
                
        """
        self.description = description
    
    def __repr__(self):
        return "<interface.Attribute - '%s'>" % self.description
        
def validate(interface, obj, members=[], meta=['interface', 'label']):
    """
    A wrapper to validate interfaces.
    
    Required Arguments:
    
        interface
            The interface class to validate against
            
        obj
            The object to validate.

    Optional Arguments:
                
        members
            The object members that must exist.
            
        meta
            The meta object members that must exist.
            
    """
    invalid = []

    if hasattr(obj, '_meta') and interface != obj._meta.interface:
        raise exc.CementInterfaceError("%s does not implement %s." % \
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
        raise exc.CementInterfaceError("Invalid or missing: %s in %s" % \
                                      (invalid, obj))