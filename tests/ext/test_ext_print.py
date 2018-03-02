
from cement.utils.test import TestApp


class PrintApp(TestApp):
    class Meta:
        extensions = ['print']
        output_handler = 'print'


class PrintDictApp(TestApp):
    class Meta:
        extensions = ['print']
        output_handler = 'print_dict'


def test_print_dict_output_handler():
    with PrintDictApp() as app:
        app.run()
        res = app.render(dict(foo='bar'))
        assert res == 'foo: bar\n'


def test_print_output_handler():
    with PrintApp() as app:
        app.run()
        res = app.render(dict(out='this is the foo bar output'))
        assert res == 'this is the foo bar output\n'

        # coverage
        app.render({})


def test_print():
    with PrintApp() as app:
        app.run()
        app.print('This is a simple output message')
        assert app.last_rendered[1] == 'This is a simple output message\n'
