"""cement-tests-073 exception classes."""

class cement-tests-073Error(Exception):
    """Generic errors."""
    def __init__(self, value, code=1):
        Exception.__init__(self)
        self.msg = value
        self.code = code
    
    def __str__(self):
        return self.msg
        
class cement-tests-073ConfigError(cement-tests-073Error):
    """Config parsing and setup errors."""
    def __init__(self, value):
        code = 10
        cement-tests-073Error.__init__(self, value, code)

class cement-tests-073RuntimeError(cement-tests-073Error):
    """Runtime errors."""
    def __init__(self, value):
        code = 20
        cement-tests-073Error.__init__(self, value, code)
        
class cement-tests-073InternalServerError(cement-tests-073Error):
    """Unknown or private internal errors."""
    def __init__(self, value):
        code = 30
        cement-tests-073Error.__init__(self, value, code)
        
class cement-tests-073ArgumentError(cement-tests-073Error):
    """Argument errors."""
    def __init__(self, value):
        code = 40
        cement-tests-073Error.__init__(self, value, code)
