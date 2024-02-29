"""
Cement smtp extension module.
"""

import os
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from ..core import mail
from ..utils import fs
from ..utils.misc import minimal_logger, is_true


LOG = minimal_logger(__name__)


class SMTPMailHandler(mail.MailHandler):

    """
    This class implements the :ref:`IMail <cement.core.mail>`
    interface, and is based on the `smtplib
    <http://docs.python.org/dev/library/smtplib.html>`_ standard library.

    """

    class Meta:

        """Handler meta-data."""

        #: Unique identifier for this handler
        label = 'smtp'

        #: Configuration default values
        config_defaults = {
            'to': [],
            'from_addr': 'noreply@localhost',
            'cc': [],
            'bcc': [],
            'subject': None,
            'subject_prefix': None,
            'host': 'localhost',
            'port': '25',
            'timeout': 30,
            'ssl': False,
            'tls': False,
            'auth': False,
            'username': None,
            'password': None,
            'files': None,
        }

    def _get_params(self, **kw):
        params = dict()

        # some keyword args override configuration defaults
        for item in ['to', 'from_addr', 'cc', 'bcc', 'subject',
                     'subject_prefix', 'files']:
            config_item = self.app.config.get(self._meta.config_section, item)
            params[item] = kw.get(item, config_item)

        # others don't
        other_params = ['ssl', 'tls', 'host', 'port', 'auth', 'username',
                        'password', 'timeout']
        for item in other_params:
            params[item] = self.app.config.get(self._meta.config_section,
                                               item)

        return params

    def send(self, body, **kw):
        """
        Send an email message via SMTP.  Keyword arguments override
        configuration defaults (cc, bcc, etc).

        Args:
            body (tuple): The message body to send. Tuple is treated as:
                ``(<text>, <html>)``. If a single string is passed it will be
                converted to ``(<text>)``. At minimum, a text version is
                required.

        Keyword Args:
            to (list): List of recipients (generally email addresses)
            from_addr (str): Address (generally email) of the sender
            cc (list): List of CC Recipients
            bcc (list): List of BCC Recipients
            subject (str): Message subject line
            subject_prefix (str): Prefix for message subject line (useful to
                override if you want to remove/change the default prefix).
            files (list): List of file paths to attach to the message. Can be
                ``[ '/path/to/file.ext', ... ]`` or alternative filename can
                be defined by passing a list of tuples in the form of
                ``[ ('alt-name.ext', '/path/to/file.ext'), ...]``

        Returns:
            bool:``True`` if message is sent successfully, ``False`` otherwise

        Example:

            .. code-block:: python

                # Using all configuration defaults
                app.mail.send('This is my message body')

                # Overriding configuration defaults
                app.mail.send('My message body'
                    from_addr='me@example.com',
                    to=['john@example.com'],
                    cc=['jane@example.com', 'rita@example.com'],
                    subject='This is my subject',
                    )

        """
        params = self._get_params(**kw)

        if is_true(params['ssl']):
            server = smtplib.SMTP_SSL(params['host'], params['port'],
                                      params['timeout'])
            LOG.debug("%s : initiating smtp over ssl" % self._meta.label)

        else:
            server = smtplib.SMTP(params['host'], params['port'],
                                  params['timeout'])
            LOG.debug("%s : initiating smtp" % self._meta.label)

        if self.app.debug is True:
            server.set_debuglevel(9)

        if is_true(params['tls']):
            LOG.debug("%s : initiating tls" % self._meta.label)
            server.starttls()

        if is_true(params['auth']):
            server.login(params['username'], params['password'])

        self._send_message(server, body, **params)
        server.quit()

    def _send_message(self, server, body, **params):
        msg = MIMEMultipart('alternative')
        msg.set_charset('utf-8')

        msg['From'] = params['from_addr']
        msg['To'] = ', '.join(params['to'])
        if params['cc']:
            msg['Cc'] = ', '.join(params['cc'])
        if params['bcc']:
            msg['Bcc'] = ', '.join(params['bcc'])
        if params['subject_prefix'] not in [None, '']:
            subject = '%s %s' % (params['subject_prefix'],
                                 params['subject'])
        else:
            subject = params['subject']
        msg['Subject'] = Header(subject)

        # add body as text and/or as html
        partText = None
        partHtml = None

        if type(body) not in [str, tuple]:
            error_msg = "Message body must be string or tuple " \
                        "('<text>', '<html>')"
            raise TypeError(error_msg)

        if isinstance(body, str):
            partText = MIMEText(body)
        elif isinstance(body, tuple):
            # handle plain text
            if len(body) >= 1:
                partText = MIMEText(body[0], 'plain')

            # handle html
            if len(body) >= 2:
                partHtml = MIMEText(body[1], 'html')

        if partText:
            msg.attach(partText)
        if partHtml:
            msg.attach(partHtml)

        # attach files
        if params['files']:
            for in_path in params['files']:
                part = MIMEBase('application', 'octet-stream')

                # support for alternative file name if its tuple
                # like ('alt-name.ext', '/path/to/file.ext')
                if isinstance(in_path, tuple):
                    if in_path[0] == in_path[1]:
                        # protect against the full path being passed in
                        alt_name = os.path.basename(in_path[0])
                    else:
                        alt_name = in_path[0]
                    path = in_path[1]
                else:
                    alt_name = os.path.basename(in_path)
                    path = in_path

                path = fs.abspath(path)

                # add attachment
                with open(path, 'rb') as file:
                    part.set_payload(file.read())

                # encode and name
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename={alt_name}',
                )
                msg.attach(part)

        server.send_message(msg)


def load(app):
    app.handler.register(SMTPMailHandler)
