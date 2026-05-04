
from __future__ import annotations

from cement import App, CaughtSignal  # noqa: E402
from cement.core.exc import FrameworkError

from .controllers.base import Base  # noqa: E402


class CementApp(App):
    class Meta:
        label = 'cement'
        controller = 'base'
        template_module = 'cement.cli.templates'
        template_handler = 'jinja2'
        config_handler = 'yaml'
        config_file_suffix = '.yml'

        extensions = [
            'generate',
            'yaml',
            'jinja2',
        ]

        handlers = [
            Base,
        ]


class CementTestApp(CementApp):
    class Meta:
        argv: list[str] = []
        config_files: list[str] = []
        exit_on_close = False


def main(argv: list[str] | None = None) -> None:
    # Issue #679: https://github.com/datafolklabs/cement/issues/679
    try:
        import jinja2  # noqa: F401
        import yaml  # type: ignore  # noqa: F401
    except ModuleNotFoundError as e:  # pragma: nocover
        raise FrameworkError('Cement CLI Dependencies are missing! Install cement[cli] extras ' +
                             'package to resolve -> pip install cement[cli]') from e

    with CementApp() as app:
        try:
            app.run()
        except AssertionError as e:  # pragma: nocover
            # noqa: T201 - intentional CLI error output
            print(f'AssertionError > {e.args[0]}')  # pragma: nocover  # noqa: T201
            app.exit_code = 1  # pragma: nocover
        except CaughtSignal as e:  # pragma: nocover
            # noqa: T201 - intentional CLI signal output
            print(f'\n{e}')  # pragma: nocover  # noqa: T201
            app.exit_code = 0  # pragma: nocover


if __name__ == '__main__':
    main()                                              # pragma: nocover
