#!/usr/bin/env python

import platform

from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose


class CementDevtoolsController(CementBaseController):
    class Meta:
        label = 'base'
        arguments = [
            (['modifier1'], 
             dict(help='command modifier positional argument', nargs='?')),
        ]
        
    @expose(hide=True) 
    def default(self):
        raise NotImplementedError
    
    @expose(help='bump the release version', aliases=['bump'])
    def bump_version(self):
        assert self.app.pargs.modifier1, "A positional argument is required."
        
        parts = self.app.pargs.modifier1.split('.')
        major_ver = "%s.%s" % (parts[0], parts[1])
        full_ver = '.'.join(parts)
     
        if platform.system() == 'Darwin':
            pass
        else:
            
        
    @expose(help='create a cement release')
    def make_release(self):
        pass

class CementDevtoolsApp(CementApp):
    class Meta:
        label = 'cement-devtools'
        base_controller = CementDevtoolsController
        
                
def main():
    app = CementDevtoolsApp('cement-devtools')
    try:
        app.setup()
        app.run()
    except AssertionError as e:
        print "AssertionError => %s" % e.args[0]
    finally:
        app.close()

if __name__ == '__main__':
    main()