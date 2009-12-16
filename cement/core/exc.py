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
        code = 10
        CementError.__init__(self, value, code)

        
class CementRuntimeError(CementError):
    """Runtime errors."""
    def __init__(self, value):
        code = 20
        CementError.__init__(self, value, code)
        
class CementInternalServerError(CementError):
    """Unknown or private internal errors."""
    def __init__(self, value):
        code = 30
        CementError.__init__(self, value, code)
        
class CementArgumentError(CementError):
    """Argument errors."""
    def __init__(self, value):
        code = 40
        CementError.__init__(self, value, code)
    
class CementIOError(CementError):
    """IO operation errors."""
    def __init__(self, value):
        code = 50
        CementError.__init__(self, value, code)