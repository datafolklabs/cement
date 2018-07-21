
from cement import App, init_defaults
from cement.core.exc import CaughtSignal
from .core.exc import {{ class_name }}Error


# configuration defaults
DEFAULTS = init_defaults('{{ label }}')
DEFAULTS['{{ label }}']['{{ foo }}'] = 'bar'


class {{ class_name }}(App):
    """{{ name }} primary application."""

    class Meta:
        label = '{{ label }}'

        # offload handler/hook registration to a separate module
        bootstrap = '{{ label }}.bootstrap'

        # configuration defaults
        config_defaults = DEFAULTS

        # load additional framework extensions
        extensions = [
            'json',
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

        # call sys.exit() on close
        close_on_exit = True


class {{ class_name }}Test({{ class_name}}):
    """A test app that is better suited for testing."""

    class Meta:
        # default argv to empty (don't use sys.argv)
        argv = []

        # don't look for config files (could break tests)
        config_files = []

        # don't call sys.exit() when app.close() is called in tests
        exit_on_close = False


def main():
    with {{ class_name }}() as app:
        try:
            app.run()

        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except {{ class_name}}Error:
            print('{{ class_name }}Error > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()
