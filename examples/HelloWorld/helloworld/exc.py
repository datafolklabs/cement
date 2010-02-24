"""HelloWorld exception classes."""

class HelloWorldError(Exception):
    """Generic errors."""
    def __init__(self, value, code=1):
        Exception.__init__(self)
        self.msg = value
        self.code = code
    
    def __str__(self):
        return self.msg
        
class HelloWorldConfigError(HelloWorldError):
    """Config parsing and setup errors."""
    def __init__(self, value):
        code = 10
        HelloWorldError.__init__(self, value, code)

class HelloWorldRuntimeError(HelloWorldError):
    """Runtime errors."""
    def __init__(self, value):
        code = 20
        HelloWorldError.__init__(self, value, code)
        
class HelloWorldInternalServerError(HelloWorldError):
    """Unknown or private internal errors."""
    def __init__(self, value):
        code = 30
        HelloWorldError.__init__(self, value, code)
        
class HelloWorldArgumentError(HelloWorldError):
    """Argument errors."""
    def __init__(self, value):
        code = 40
        HelloWorldError.__init__(self, value, code)
