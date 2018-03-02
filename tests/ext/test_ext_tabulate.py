

from cement.utils.test import TestApp


class TabulateApp(TestApp):
    class Meta:
        extensions = ['tabulate']
        output_handler = 'tabulate'


def test_tabulate():
    with TabulateApp() as app:
        res = app.render([['John', 'Doe']], headers=['FOO', 'BAR'])
        assert res.find('FOO')
