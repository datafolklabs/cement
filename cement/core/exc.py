"""Cement exception classes."""

class CementError(Exception):
    """Generic errors."""
    def __init__(self, value, code=1):
        Exception.__init__(self)
        self.msg = value
        self.code = code
    
    def __str__(self):
        return self.msg
        
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
        
class CementInternalServerError(CementError):
    """Unknown or private internal errors."""
    def __init__(self, value):
        code = 1030
        CementError.__init__(self, value, code)
        
class CementArgumentError(CementError):
    """Argument errors."""
    def __init__(self, value):
        code = 1040
        CementError.__init__(self, value, code)
