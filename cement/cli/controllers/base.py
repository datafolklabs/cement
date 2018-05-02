
from cement import Controller


class Base(Controller):
    class Meta:
        label = 'base'
        description = 'Cement Framework Developer Tools'
        epilog = 'Example: cement generate app /path/to/myapp'

    def _default(self):
        self.app.args.print_help()
