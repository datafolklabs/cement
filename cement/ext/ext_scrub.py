"""
Cement scrub extension module.
"""

import re
from .. import Controller
from ..utils.misc import minimal_logger

LOG = minimal_logger(__name__)


def scrub_output(app, text):
    if app.pargs.scrub:
        text = app.scrub(text)
    return text


def extend_scrub(app):
    def scrub(text):
        if not hasattr(app._meta, 'scrub') or app._meta.scrub is None:
            return text  # pragma: nocover
        elif isinstance(text, str):
            for regex, replace in app._meta.scrub:
                text = re.sub(regex, replace, text)
        else:
            LOG.debug('text is not str > %s' % type(text))
        return text

    app.extend('scrub', scrub)


class ScrubController(Controller):
    """
    Add embedded options to the base controller to support scrubbing output.
    """

    class Meta:
        #: Controller label
        label = 'scrub'

        #: Parent controller to stack ontop of
        stacked_on = 'base'

        #: Stacking method
        stacked_type = 'embedded'

        #: Command line argument options
        argument_options = ['--scrub']

        #: Command line argument options help
        argument_help = 'obfuscate sensitive data from rendered output'

    def _pre_argument_parsing(self):
        if self._meta.argument_options is not None:
            assert isinstance(self._meta.argument_options, list), \
                "ScrubController.Meta.argument_options must be a list"
            self.app.args.add_argument(*self._meta.argument_options,
                                       help=self._meta.argument_help,
                                       action='store_true',
                                       dest='scrub')


def load(app):
    app.handler.register(ScrubController)
    app.hook.register('post_render', scrub_output)
    app.hook.register('pre_argument_parsing', extend_scrub)
