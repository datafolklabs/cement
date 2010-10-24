"""helloworld exception classes."""

class HelloworldError(Exception):
    """Generic errors."""
    def __init__(self, value, code=1):
        Exception.__init__(self)
        self.msg = value
        self.code = code
    
    def __str__(self):
        return self.msg
        
    def __unicode__(self):
        return unicode(self.msg)
                
class HelloworldConfigError(HelloworldError):
    """Config parsing and setup errors."""
    def __init__(self, value):
        code = 10
        HelloworldError.__init__(self, value, code)

class HelloworldRuntimeError(HelloworldError):
    """Runtime errors."""
    def __init__(self, value):
        code = 20
        HelloworldError.__init__(self, value, code)

class HelloworldArgumentError(HelloworldError):
    """Argument errors."""
    def __init__(self, value):
        code = 40
        HelloworldError.__init__(self, value, code)
