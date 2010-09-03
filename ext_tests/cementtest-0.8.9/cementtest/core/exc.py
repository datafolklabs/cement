"""cementtest exception classes."""

class CementTestError(Exception):
    """Generic errors."""
    def __init__(self, value, code=1):
        Exception.__init__(self)
        self.msg = value
        self.code = code
    
    def __str__(self):
        return self.msg
        
    def __unicode__(self):
        return unicode(self.msg)
                
class CementTestConfigError(CementTestError):
    """Config parsing and setup errors."""
    def __init__(self, value):
        code = 10
        CementTestError.__init__(self, value, code)

class CementTestRuntimeError(CementTestError):
    """Runtime errors."""
    def __init__(self, value):
        code = 20
        CementTestError.__init__(self, value, code)
        
class CementTestInternalServerError(CementTestError):
    """Unknown or private internal errors."""
    def __init__(self, value):
        code = 30
        CementTestError.__init__(self, value, code)
        
class CementTestArgumentError(CementTestError):
    """Argument errors."""
    def __init__(self, value):
        code = 40
        CementTestError.__init__(self, value, code)
