"""helloworld exception classes."""

class helloworldError(Exception):
    """Generic errors."""
    def __init__(self, value, code=1):
        Exception.__init__(self)
        self.msg = value
        self.code = code
    
    def __str__(self):
        return self.msg
        
class helloworldConfigError(helloworldError):
    """Config parsing and setup errors."""
    def __init__(self, value):
        code = 10
        helloworldError.__init__(self, value, code)

class helloworldRuntimeError(helloworldError):
    """Runtime errors."""
    def __init__(self, value):
        code = 20
        helloworldError.__init__(self, value, code)
        
class helloworldInternalServerError(helloworldError):
    """Unknown or private internal errors."""
    def __init__(self, value):
        code = 30
        helloworldError.__init__(self, value, code)
        
class helloworldArgumentError(helloworldError):
    """Argument errors."""
    def __init__(self, value):
        code = 40
        helloworldError.__init__(self, value, code)
