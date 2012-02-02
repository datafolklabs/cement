"""Cement core exceptions module."""

class CementError(Exception):
    """Generic errors."""
    def __init__(self, msg):
        Exception.__init__(self)
        self.msg = msg
    
    def __str__(self):
        return self.msg

            
class CementConfigError(CementError):
    pass

class CementRuntimeError(CementError):
    pass
        
class CementArgumentError(CementError):
    pass

class CementInterfaceError(CementError):
    pass
    
class CementSignalError(CementError):
    """Signal errors."""
    def __init__(self, signum, frame):
        msg = 'Caught signal %s' % signum
        super(CementSignalError, self).__init__(msg)
        self.signum = signum
        self.frame = frame        