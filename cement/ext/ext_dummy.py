"""
Cement dummy extension module.
"""

from ..core.output import OutputHandler
from ..core.template import TemplateHandler
from ..core.mail import MailHandler
from ..utils.misc import minimal_logger

LOG = minimal_logger(__name__)


class DummyOutputHandler(OutputHandler):

    """
    This class is an internal implementation of the
    :class:`cement.core.output.OutputHandlerBase` interface. It does not take
    any parameters on initialization, and does not actually output anything.

    """
    class Meta:

        """Handler meta-data"""

        #: The string identifier of this handler.
        label = 'dummy'

        #: Whether or not to include ``dummy`` as an available to choice
        #: to override the ``output_handler`` via command line options.
        overridable = False

    def render(self, data, template=None, **kw):
        """
        This implementation does not actually render anything to output, but
        rather logs it to the debug facility.

        Args:
            data (dict): The data dictionary to render.

        Keyword Args:
            template (str): The template parameter is not used by this
                implementation at all.

        """
        LOG.debug("not rendering any output to console")
        LOG.debug("DATA: %s" % data)
        return None


class DummyTemplateHandler(TemplateHandler):

    """
    This class is an internal implementation of the
    :class:`cement.core.template.TemplateHandlerBase` interface. It does not
    take any parameters on initialization, and does not actually render
    anything.

    """
    class Meta:

        """Handler meta-data"""

        #: The string identifier of this handler.
        label = 'dummy'

    def render(self, content, data, *args, **kw):
        """
        This implementation does not actually render anything, but
        rather logs it to the debug facility.

        Args:
            content (str): The content to render as dictionary
            data (dict): The data dictionary to render.

        """
        LOG.debug("CONTENT: %s" % content)
        LOG.debug("DATA: %s" % data)
        return None

    def copy(self, src, dest, data):
        """
        This implementation does not actually copy anything, but rather logs it
        to the debug facility.

        Args:
            src (str): The source template directory.
            dest (str): The destination directory.
            data (dict): The data dictionary to render with templates.
        """
        LOG.debug("COPY: %s -> %s" % (src, dest))


class DummyMailHandler(MailHandler):

    """
    This class implements the :class:`cement.core.mail.IMail`
    interface, but is intended for use in development as no email is actually
    sent.

    Example:

    .. code-block:: python

        class MyApp(App):
            class Meta:
                label = 'myapp'
                mail_handler = 'dummy'

        with MyApp() as app:
            app.run()

            app.mail.send('This is my fake message',
                subject='This is my subject',
                to=['john@example.com', 'rita@example.com'],
                from_addr='me@example.com',
                )

    The above will print the following to console:

    .. code-block:: text

        ======================================================================
        DUMMY MAIL MESSAGE
        ----------------------------------------------------------------------

        To: john@example.com, rita@example.com
        From: me@example.com
        CC:
        BCC:
        Subject: This is my subject

        ---

        This is my fake message

        ----------------------------------------------------------------------

    **Configuration**

    This handler supports the following configuration settings:

     * **to** - Default ``to`` addresses (list, or comma separated depending
       on the ConfigHandler in use)
     * **from_addr** - Default ``from_addr`` address
     * **cc** - Default ``cc`` addresses (list, or comma separated depending
       on the ConfigHandler in use)
     * **bcc** - Default ``bcc`` addresses (list, or comma separated depending
       on the ConfigHandler in use)
     * **subject** - Default ``subject``
     * **subject_prefix** - Additional string to prepend to the ``subject``


    You can add these to any application configuration file under a
    ``[mail.dummy]`` section, for example:

    **~/.myapp.conf**

    .. code-block:: text

        [myapp]

        # set the mail handler to use
        mail_handler = dummy


        [mail.dummy]

        # default to addresses (comma separated list)
        to = me@example.com

        # default from address
        from = someone_else@example.com

        # default cc addresses (comma separated list)
        cc = jane@example.com, rita@example.com

        # default bcc addresses (comma separated list)
        bcc = blackhole@example.com, someone_else@example.com

        # default subject
        subject = This is The Default Subject

        # additional prefix to prepend to the subject
        subject_prefix = MY PREFIX >

    """

    class Meta:

        """Handler meta-data."""

        #: Unique identifier for this handler
        label = 'dummy'

    def _get_params(self, **kw):
        params = dict()
        for item in ['to', 'from_addr', 'cc', 'bcc', 'subject']:
            config_item = self.app.config.get(self._meta.config_section, item)
            params[item] = kw.get(item, config_item)

        # also grab the subject_prefix
        params['subject_prefix'] = self.app.config.get(
            self._meta.config_section,
            'subject_prefix'
        )

        return params

    def send(self, body, **kw):
        """
        Mimic sending an email message, but really just print what would be
        sent to console.  Keyword arguments override configuration
        defaults (cc, bcc, etc).

        Args:
            body: The message body to send

        Keyword Args:
            to (list): List of recipients (generally email addresses)
            from_addr (str): Address (generally email) of the sender
            cc (list): List of CC Recipients
            bcc (list): List of BCC Recipients
            subject (str): Message subject line

        Returns:
            bool:``True`` if message is sent successfully, ``False`` otherwise

        Example:

            .. code-block:: python

                # Using all configuration defaults
                app.mail.send('This is my message body')

                # Overriding configuration defaults
                app.mail.send('My message body'
                    to=['john@example.com'],
                    from_addr='me@example.com',
                    cc=['jane@example.com', 'rita@example.com'],
                    subject='This is my subject',
                    )

        """
        # shorted config values
        params = self._get_params(**kw)
        msg = "\n" + "=" * 77 + "\n"
        msg += "DUMMY MAIL MESSAGE\n"
        msg += "-" * 77 + "\n\n"
        msg += "To: %s\n" % ', '.join(params['to'])
        msg += "From: %s\n" % params['from_addr']
        msg += "CC: %s\n" % ', '.join(params['cc'])
        msg += "BCC: %s\n" % ', '.join(params['bcc'])

        if params['subject_prefix'] not in [None, '']:
            msg += "Subject: %s %s\n\n---\n\n" % (params['subject_prefix'],
                                                  params['subject'])
        else:
            msg += "Subject: %s\n\n---\n\n" % params['subject']
        msg += body + "\n"

        msg += "\n" + "-" * 77 + "\n"

        print(msg)
        return True


def load(app):
    app.handler.register(DummyOutputHandler)
    app.handler.register(DummyTemplateHandler)
    app.handler.register(DummyMailHandler)
