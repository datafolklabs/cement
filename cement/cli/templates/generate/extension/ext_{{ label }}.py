
from typing import TYPE_CHECKING

from cement import minimal_logger

if TYPE_CHECKING:
    from cement import App  # pragma: nocover

LOG = minimal_logger(__name__)

def {{ label }}_pre_run_hook(app: "App") -> None:
    # do something with app
    LOG.debug('Inside {{ label }}_pre_run_hook!')

def load(app: "App") -> None:
    # do something to extend cement
    app.hook.register('pre_run', {{ label }}_pre_run_hook)
