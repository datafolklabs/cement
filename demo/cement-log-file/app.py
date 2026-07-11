"""Minimal Cement app used to demonstrate CEMENT_FRAMEWORK_LOG_FILE (issue #593).

Running this app does nothing interesting on its own. The point is that when
framework logging is enabled (CEMENT_LOG=1), Cement's internal minimal_logger
emits debug output during setup/run/close -- and when CEMENT_FRAMEWORK_LOG_FILE
is also set, that same output is written to the given file in addition to the
console.
"""

from cement import App


class MyApp(App):
    class Meta:
        label = 'myapp'


if __name__ == '__main__':
    with MyApp() as app:
        app.run()
