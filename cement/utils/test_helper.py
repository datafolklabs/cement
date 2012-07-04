
import sys
from ..core import backend, foundation, handler, hook

class TestApp(foundation.CementApp):
    class Meta:
        config_files = []
        argv = []
            
    def setup(self):
        super(TestApp, self).setup()

def reset_backend():
    for _handler in backend.handlers.copy():
        del backend.handlers[_handler]
    for _hook in backend.hooks.copy():
        del backend.hooks[_hook]

def prep(label='test', *args, **kw):
    reset_backend()
    dummy_app = TestApp(label, *args, **kw)
    return dummy_app

