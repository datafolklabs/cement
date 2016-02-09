from time import sleep
from cement.core.exc import CaughtSignal
from cement.core import hook
from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose

def print_foo(app):
    print("Foo => %s" % app.config.get('myapp', 'foo'))


class Base(CementBaseController):
    class Meta:
        label = 'base'

    @expose(hide=True)
    def default(self):
        print('Inside Base.default()')

        # simulate a long running process
        while True:
            sleep(30)

class MyApp(CementApp):
    class Meta:
        label = 'myapp'
        base_controller = Base
        extensions = ['reload_config']


with MyApp() as app:
    # run this anytime the configuration has changed
    hook.register('post_reload_config', print_foo)

    try:
        app.run()
    except CaughtSignal as e:
        # maybe do something... but catch it regardless so app.close() is
        # called when exiting `with` cleanly.
        print(e)
