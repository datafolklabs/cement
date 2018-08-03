"""
Cement scrub extension module.
"""

import re
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

    if hasattr(app._meta, 'scrub_argument'):
        arg = app._meta.scrub_argument
    else:
        arg = ['--scrub']

    if hasattr(app._meta, 'scrub_argument_help'):
        arg_help = app._meta.scrub_argument_help
    else:
        arg_help = 'obfuscate sensitive data from output'

    app.args.add_argument(*arg,
                          help=arg_help,
                          action='store_true',
                          dest='scrub')


def load(app):
    app.hook.register('post_render', scrub_output)
    app.hook.register('pre_argument_parsing', extend_scrub)
