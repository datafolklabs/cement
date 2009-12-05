
class CementError(Exception):
    def __init__(self, value, code=1):
        self.msg = value
        self.code = code
    
    def __str__(self):
        return self.msg
        
class CementConfigError(CementError):
    def __init__(self, value):
        code = 10
        CementError.__init__(self, value, code)
        
class CementRuntimeError(CementError):
    def __init__(self, value):
        code = 20
        CementError.__init__(self, value, code)
        
class CementInternalServerError(CementError):
    def __init__(self, value):
        code = 30
        CementError.__init__(self, value, code)
        
class CementArgumentError(CementError):
    def __init__(self, value):
        code = 40
        CementError.__init__(self, value, code)
    
class CementIOError(CementError):
    def __init__(self, value):
        code = 50
        CementError.__init__(self, value, code)