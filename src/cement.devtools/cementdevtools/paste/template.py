"""
Definition for Cement laycement templates.

A significant portion of this file was derived from the tg.devtools software
which is licensed under the MIT license.  The following license applies to
the work in *this* file only, and not any other part of the Cement Framework
unless otherwise noted:

-----------------------------------------------------------------------------
Copyright (c) 2008 TurboGears Team

 Permission is hereby granted, free of charge, to any person
 obtaining a copy of this software and associated documentation
 files (the "Software"), to deal in the Software without
 restriction, including without limitation the rights to use,
 copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the
 Software is furnished to do so, subject to the following
 conditions:

 The above copyright notice and this permission notice shall be
 included in all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 OTHER DEALINGS IN THE SOFTWARE.
-----------------------------------------------------------------------------
"""

from paste.script import templates
from tempita import paste_script_template_renderer

class CementAppTemplate(templates.Template):
    """
    Cement default paste template class
    """
    _template_dir = 'templates/cementapp'
    template_renderer = staticmethod(paste_script_template_renderer)
    summary = 'Cement Standard Template'
    egg_plugins = ['PasteScript', 'cement']
    vars = [
        templates.var("package", "Package module name", default=''),
        templates.var("cement_version", "Cement version", default=0.8),
        templates.var("cement_next_version", "Cement Next Version", 
                      default=2.0),
        templates.var("description", "Description", default=''),
        templates.var("creator", "Creator", default=''),
        templates.var("creator_email", "Creator Email", default=''),
        templates.var("url", "URL", default=''),
        templates.var("license", "License", default=''),
        ]

    def pre(self, command, output_dir, vars):
        """Called before template is applied."""
        pass

class CementPluginTemplate(templates.Template):
    """
    Cement plugin default paste template class.
    """
    _template_dir = 'templates/cementplugin'
    template_renderer = staticmethod(paste_script_template_renderer)
    summary = 'Cement Plugin Standard Template'
    egg_plugins = ['PasteScript', 'cement']
    vars = [
        templates.var("plugin", "cement plugin name", default=None),
        templates.var("project", "Parent application this plugin is for", 
                      default=None),
        templates.var("package", "Package module name", default=''),
        templates.var("cement_version", "Cement version", default=0.8),
        templates.var("cement_next_version", "Cement Next Version", 
                      default=2.0),
        templates.var("creator", "Creator", default=''),
        templates.var("creator_email", "Creator Email", default=''),
        templates.var("url", "URL", default=''),
        templates.var("license", "License", default=''),
        ]

    def pre(self, command, output_dir, vars):
        """Called before template is applied."""
        pass
