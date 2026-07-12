
from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal

from .controllers.base import Base
from .core.exc import {{ class_name }}Error

# configuration defaults
CONFIG = init_defaults('{{ label }}')
CONFIG['{{ label }}']['foo'] = 'bar'


class {{ class_name }}(App):
    """{{ name }} primary application."""

    class Meta:
        label = '{{ label }}'

        # configuration defaults
        config_defaults = CONFIG

        # call sys.exit() on close
        exit_on_close = True

        # load additional framework extensions
        extensions = [
            'yaml',
            'colorlog',
            'jinja2',
        ]

        # configuration handler
        config_handler = 'yaml'

        # configuration file suffix
        config_file_suffix = '.yml'

        # set the log handler
        log_handler = 'colorlog'

        # set the output handler
        output_handler = 'jinja2'

        # register handlers
        handlers = [
            Base
        ]


class {{ class_name }}Test(TestApp,{{ class_name }}):
    """A sub-class of {{ class_name }} that is better suited for testing."""

    class Meta:
        label = '{{ label }}'


def main() -> None:
    with {{ class_name }}() as app:
        try:
            app.run()

        except AssertionError as e:
            print(f'AssertionError > {e.args[0]}')
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except {{ class_name }}Error as e:
            print(f'{{ class_name }}Error > {e.args[0]}')
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print(f'\n{e}')
            app.exit_code = 0


if __name__ == '__main__':
    main()
