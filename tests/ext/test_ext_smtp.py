
import os
import mock
import requests
import json
from time import sleep
from pytest import raises
from cement.utils.test import TestApp
from cement.utils.misc import init_defaults

if 'SMTP_HOST' in os.environ.keys():
    smtp_host = os.environ['SMTP_HOST']
else:
    smtp_host = 'mailpit'


mailpit_api = f'http://{smtp_host}:8025/api/v1'
defaults = init_defaults('mail.smtp')
defaults['mail.smtp']['host'] = smtp_host
defaults['mail.smtp']['port'] = 1025
defaults['mail.smtp']['to'] = 'noreply@localhost'
defaults['mail.smtp']['from_addr'] = 'nobody@localhost'
defaults['mail.smtp']['subject_prefix'] = 'UNIT TEST >'


class SMTPApp(TestApp):
    class Meta:
        extensions = ['smtp']
        mail_handler = 'smtp'


def delete_msg(message_id):
    payload = {
        "ids": [
            message_id
        ]
    }
    payload = json.dumps(payload)

    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
    }
    requests.delete(f"{mailpit_api}/messages", data=payload, headers=headers)


def test_smtp_send(rando):
    defaults['mail.smtp']['subject'] = rando

    with SMTPApp(config_defaults=defaults) as app:
        app.run()

        app.mail.send(f"{rando}",
                      to=[f'to-{rando}@localhost'],
                      from_addr=f'from-{rando}@localhost')
        res = requests.get(f"{mailpit_api}/search?query={rando}")
        data = res.json()
        assert len(data['messages']) == 1
        msg = data['messages'][0]

        assert msg['From']['Address'] == f'from-{rando}@localhost'
        assert msg['To'][0]['Address'] == f'to-{rando}@localhost'
        assert msg['Subject'] == f'UNIT TEST > {rando}'
        assert msg['Attachments'] == 0
        assert msg['Cc'] == []
        assert msg['Bcc'] == []

        delete_msg(msg['ID'])


def test_smtp_html(rando):
    defaults['mail.smtp']['subject'] = rando

    with SMTPApp(config_defaults=defaults) as app:
        app.run()

        app.mail.send((f"{rando}", f"<body>{rando}</body>"))
        sleep(3)
        res = requests.get(f"{mailpit_api}/search?query={rando}")
        data = res.json()
        assert len(data['messages']) == 1
        msg = data['messages'][0]

        text_url = f"http://{smtp_host}:8025/view/{msg['ID']}.txt"
        res_text = requests.get(text_url)
        assert res_text.content.decode('utf-8') == rando

        html_url = f"http://{smtp_host}:8025/view/{msg['ID']}.html"
        res_html = requests.get(html_url)
        assert res_html.content.decode('utf-8') == f"<body>{rando}</body>"

        delete_msg(msg['ID'])


def test_smtp_html_bad_body_type(rando):
    defaults['mail.smtp']['subject'] = rando

    with SMTPApp(config_defaults=defaults) as app:
        app.run()

        error_msg = '(.*)Message body must be string or tuple(.*)'
        with raises(TypeError, match=error_msg):
            app.mail.send(['text', '<body>html</body>'])


def test_smtp_cc_bcc(rando):
    defaults['mail.smtp']['subject'] = rando

    with SMTPApp(config_defaults=defaults) as app:
        app.run()

        cc = [f"cc1-{rando}@localhost", f"cc2-{rando}@localhost"]
        bcc = [f"bcc1-{rando}@localhost", f"bcc2-{rando}@localhost"]
        app.mail.send(f"{rando}",
                      cc=cc,
                      bcc=bcc)
        res = requests.get(f"{mailpit_api}/search?query={rando}")
        data = res.json()
        assert len(data['messages']) == 1
        msg = data['messages'][0]

        cc_verify = [x['Address'] for x in msg['Cc']]
        bcc_verify = [x['Address'] for x in msg['Bcc']]
        assert f"cc1-{rando}@localhost" in cc_verify
        assert f"cc2-{rando}@localhost" in cc_verify
        assert f"bcc1-{rando}@localhost" in bcc_verify
        assert f"bcc2-{rando}@localhost" in bcc_verify

        delete_msg(msg['ID'])


def test_smtp_files(rando, tmp):
    defaults['mail.smtp']['subject'] = rando

    with SMTPApp(config_defaults=defaults) as app:
        app.run()

        files = []
        for iter in [1, 2, 3]:
            _file = f"{tmp.file}-{iter}"
            with open(_file, 'w') as _open_file:
                _open_file.write(f"{rando}-{iter}")
            files.append(_file)

        app.mail.send(f"{rando}", files=files)
        sleep(3)
        res = requests.get(f"{mailpit_api}/search?query={rando}")
        data = res.json()
        assert len(data['messages']) == 1
        msg = data['messages'][0]

        assert msg['Attachments'] == 3

        delete_msg(msg['ID'])


def test_smtp_files_alt_name(rando, tmp):
    defaults['mail.smtp']['subject'] = rando

    with SMTPApp(config_defaults=defaults) as app:
        app.run()

        files = [(f"alt-filename-{rando}", tmp.file)]
        app.mail.send(f"{rando}", files=files)
        sleep(3)
        res = requests.get(f"{mailpit_api}/search?query={rando}")
        data = res.json()
        assert len(data['messages']) == 1
        msg = data['messages'][0]

        assert msg['Attachments'] == 1

        res_full = requests.get(f"{mailpit_api}/message/{msg['ID']}")
        data = res_full.json()
        assert data['Attachments'][0]['FileName'] == f"alt-filename-{rando}"
        delete_msg(msg['ID'])


def test_smtp_files_path_does_not_exist(rando, tmp):
    defaults['mail.smtp']['subject'] = rando

    with SMTPApp(config_defaults=defaults) as app:
        app.run()

        files = [(f"{tmp.file}-does-not-exist")]

        with raises(FileNotFoundError):
            app.mail.send(f"{rando}", files=files)


def test_smtp_files_alt_name_is_path(rando, tmp):
    # ensure only the basename of file is set if full path is passed as alt
    # name
    defaults['mail.smtp']['subject'] = rando

    with SMTPApp(config_defaults=defaults) as app:
        app.run()

        files = [(tmp.file, tmp.file)]
        app.mail.send(f"{rando}", files=files)
        sleep(3)
        res = requests.get(f"{mailpit_api}/search?query={rando}")
        data = res.json()
        assert len(data['messages']) == 1
        msg = data['messages'][0]

        assert msg['Attachments'] == 1

        res_full = requests.get(f"{mailpit_api}/message/{msg['ID']}")
        data = res_full.json()
        assert data['Attachments'][0]['FileName'] == os.path.basename(tmp.file)
        delete_msg(msg['ID'])


def test_smtp_tls(rando):
    defaults['mail.smtp']['subject'] = rando
    defaults['mail.smtp']['tls'] = True

    with SMTPApp(config_defaults=defaults, debug=True) as app:
        app.run()
        app.mail.send(rando)
        res = requests.get(f"{mailpit_api}/search?query={rando}")
        data = res.json()
        assert len(data['messages']) == 1
        msg = data['messages'][0]

        delete_msg(msg['ID'])


# FIXME: need to replace old mocks with mailpit tests

def test_mock_smtp_defaults():
    defaults = init_defaults('mail.smtp')
    defaults['mail.smtp']['to'] = 'test_smtp_defaults@localhost'
    defaults['mail.smtp']['from_addr'] = 'nobody@localhost'
    defaults['mail.smtp']['cc'] = 'nobody@localhost'
    defaults['mail.smtp']['bcc'] = 'nobody@localhost'
    defaults['mail.smtp']['subject'] = 'test_smtp_defaults'
    defaults['mail.smtp']['subject_prefix'] = 'UNIT TEST >'

    with mock.patch('smtplib.SMTP') as mock_smtp:
        with SMTPApp(config_defaults=defaults) as app:
            app.run()
            app.mail.send('TEST MESSAGE')

            instance = mock_smtp.return_value
            assert instance.send_message.call_count == 1


def test_mock_smtp_ssl():
    defaults = init_defaults('mail.smtp')
    defaults['mail.smtp']['ssl'] = True
    defaults['mail.smtp']['tls'] = True
    defaults['mail.smtp']['port'] = 25
    defaults['mail.smtp']['subject'] = 'test_smtp_ssl'
    defaults['mail.smtp']['subject_prefix'] = 'UNIT TEST >'

    with mock.patch('smtplib.SMTP_SSL') as mock_smtp:
        with SMTPApp(config_defaults=defaults, debug=True) as app:
            app.run()
            app.mail.send('TEST MESSAGE',
                          to=['test_smtp_ssl@localhost'],
                          from_addr='noreply@localhost')

            instance = mock_smtp.return_value
            assert instance.send_message.call_count == 1


def test_mock_smtp_tls_no_ssl():
    defaults = init_defaults('mail.smtp')
    defaults['mail.smtp']['ssl'] = False
    defaults['mail.smtp']['tls'] = True
    defaults['mail.smtp']['port'] = 25
    defaults['mail.smtp']['subject'] = 'test_smtp_tls_no_ssl'
    defaults['mail.smtp']['subject_prefix'] = 'UNIT TEST >'

    with mock.patch('smtplib.SMTP') as mock_smtp:
        with SMTPApp(config_defaults=defaults, debug=True) as app:
            app.run()
            app.mail.send('TEST MESSAGE',
                          to=['test_smtp_tls_no_ssl@localhost'],
                          from_addr='noreply@localhost')

            instance = mock_smtp.return_value
            assert instance.send_message.call_count == 1
            assert instance.starttls.call_count == 1


def test_mock_smtp_tls_over_ssl():
    defaults = init_defaults('mail.smtp')
    defaults['mail.smtp']['ssl'] = True
    defaults['mail.smtp']['tls'] = True
    defaults['mail.smtp']['port'] = 25
    defaults['mail.smtp']['subject'] = 'test_smtp_tls_over_ssl'
    defaults['mail.smtp']['subject_prefix'] = 'UNIT TEST >'

    with mock.patch('smtplib.SMTP_SSL') as mock_smtp:
        with SMTPApp(config_defaults=defaults, debug=True) as app:
            app.run()
            app.mail.send('TEST MESSAGE',
                          to=['test_smtp_tls_no_ssl@localhost'],
                          from_addr='noreply@localhost')

            instance = mock_smtp.return_value
            assert instance.send_message.call_count == 1
            assert instance.starttls.call_count == 1


def test_mock_smtp_auth(rando):
    defaults = init_defaults(rando, 'mail.smtp')
    defaults[rando]['debug'] = True
    defaults['mail.smtp']['auth'] = True
    defaults['mail.smtp']['username'] = 'john.doe'
    defaults['mail.smtp']['password'] = 'password'

    with mock.patch('smtplib.SMTP') as mock_smtp:
        with SMTPApp(config_defaults=defaults) as app:
            app.run()
            app.mail.send('TEST MESSAGE',
                          to=['me@localhost'],
                          from_addr='noreply@localhost')

            instance = mock_smtp.return_value
            assert instance.login.call_count == 1
            assert instance.send_message.call_count == 1
