
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
