"""Cement core exceptions module."""

class CementError(Exception):
    """Generic errors."""
    def __init__(self, value, code=1):
        Exception.__init__(self)
        self.msg = value
        self.code = code
    
    def __str__(self):
        return self.msg
    
    def __unicode__(self):
        return unicode(self.msg)
            
class CementConfigError(CementError):
    """Config parsing and setup errors."""
    def __init__(self, value):
        code = 1010
        CementError.__init__(self, value, code)

class CementRuntimeError(CementError):
    """Runtime errors."""
    def __init__(self, value):
        code = 1020
        CementError.__init__(self, value, code)
        
class CementArgumentError(CementError):
    """Argument errors."""
    def __init__(self, value):
        code = 1030
        CementError.__init__(self, value, code)

class CementInterfaceError(CementError):
    """Argument errors."""
    def __init__(self, value):
        code = 1040
        CementError.__init__(self, value, code)