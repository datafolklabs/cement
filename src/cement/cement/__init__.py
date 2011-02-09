"""Cement top level module"""

import sys
from cement.core.configuration import namespaces, hooks, handlers

SAVED_STDOUT = sys.stdout
SAVED_STDERR = sys.stderr

class StdOutBuffer(object):
    buffer = ''
    def write(self, text):
        self.buffer += text
        
class StdErrBuffer(object):
    buffer = ''
    def write(self, text):
        self.buffer += text

# These will only be used if --quiet or --json are passed
buf_stdout = StdOutBuffer()
buf_stderr = StdErrBuffer()
