"""Definition for Cement laycement templates."""

from paste.script import templates
from tempita import paste_script_template_renderer

class CementTemplate(templates.Template):
    """
    Cement default paste template class
    """
    _template_dir = 'templates/cement'
    template_renderer = staticmethod(paste_script_template_renderer)
    summary = 'Cement Standard Template'
    egg_plugins = ['PasteScript', 'Cement']
    vars = []

    def pre(self, command, output_dir, vars):
        """Called before template is applied."""
        pass