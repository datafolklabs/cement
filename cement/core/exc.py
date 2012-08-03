"""Cement core exceptions module."""

class CementError(Exception):
    """
    Generic errors.
    
    :param msg: The error message.
    
    """
    def __init__(self, msg):
        Exception.__init__(self)
        self.msg = msg
    
    def __str__(self):
        return self.msg

class CementRuntimeError(CementError):
    """
    General runtime errors.  Similar to '500 Internal Server Error' in the
    web world.
    """
    pass

class CementInterfaceError(CementError):
    """Interface related errors."""
    pass
    
class CementSignalError(CementError):
    """
    Signal errors.  For more information regarding signals, reference the 
    `signal <http://docs.python.org/library/signal.html>`_ library.
    
    :param signum: The signal number.
    :param frame: The signal frame.
    
    """
    def __init__(self, signum, frame):
        msg = 'Caught signal %s' % signum
        super(CementSignalError, self).__init__(msg)
        self.signum = signum
        self.frame = frame        