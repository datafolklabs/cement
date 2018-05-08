
from cement.core.foundation import TestApp
from cement.utils.misc import init_defaults


def test_dummy_output():
    with TestApp() as app:
        app.run()
        app.render({'foo': 'bar'})
        assert app.last_rendered == ({'foo': 'bar'}, None)


def test_dummy_template(tmp):
    with TestApp() as app:
        app.run()

        res = app.template.render('{{ foo }}', {'foo': 'bar'})
        assert res is None

        app.template.copy('/path/to/src', '/path/to/dest', {})


def test_dummy_mail():
    with TestApp() as app:
        app.run()
        res = app.mail.send("Test",
                            to=['me@localhost'],
                            from_addr='me@localhost')
        assert res


def test_dummy_mail_with_subject_prefix():
    defaults = init_defaults('mail.dummy')
    defaults['mail.dummy']['subject_prefix'] = 'TEST PREFIX'

    with TestApp(config_defaults=defaults) as app:
        app.run()
        res = app.mail.send("Test",
                            to=['me@localhost'],
                            from_addr='me@localhost',
                            )
        assert res
