
from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController

VERSION = '0.9.1'

BANNER = """
My Awesome Application v%s
Copyright (c) 2014 John Doe Enterprises
""" % VERSION

class MyBaseController(CementBaseController):
    class Meta:
        label = 'base'
        description = 'MyApp Does Amazing Things'
        arguments = [
            (['-v', '--version'], dict(action='version', version=BANNER)),
            ]

class MyApp(CementApp):
    class Meta:
        label = 'myapp'
        base_controller = MyBaseController


def main():
    app = MyApp()
    try:
        app.setup()
        app.run()
    finally:
        app.close()

if __name__ == '__main__':
    main()
