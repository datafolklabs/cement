
from cement import init_defaults
from cement.utils.test import TestApp


class ScrubApp(TestApp):
    class Meta:
        extensions = ['scrub', 'print', 'json']
        scrub = [
            ('foo', '$$$'),
            ('bar', '***'),
        ]


def test_scrub():
    with ScrubApp(argv=['--scrub']) as app:
        app.run()
        app.print('foobar foo bar')
        assert app.last_rendered[1] == '$$$*** $$$ ***\n'

        # coverage
        assert app.scrub(None) is None


def test_argument():
    META = init_defaults('controller.scrub')
    META['controller.scrub']['argument_options'] = ['--not-scrub']
    META['controller.scrub']['argument_help'] = 'not scrub'

    class MyScrubApp(ScrubApp):
        class Meta:
            meta_defaults = META

    with MyScrubApp(argv=['--not-scrub']) as app:
        app.run()
        app.print('foobar foo bar')
        assert app.last_rendered[1] == '$$$*** $$$ ***\n'
