"""
The Generate Extension provides a mechanism for generating common content
from template directories.  Example use case would be the ability for
application developers to easily generate new plugins for their application...
or similar in other applications such as Chef Software's
``chef generate cookbook`` type utilities.

The Cement CLI uses this extension to generate apps, plugins, extensions, and
scripts for developers building their applications on the framework.

**Requirements**

 * pyYaml (``pip install pyYaml``)
 * A valid TemplateHandler must be defined at the application level via
   ``App.Meta.template_handler`` such as ``jinja2``, ``mustache``, etc.


**Configuration**

This extension does not currently honor any application configuration settings.

**App Meta Data**

This extension honors the following ``App.Meta`` options:

* **template_handler**: A handler class that implements the Template interface.
* **template_dirs**: A list of data directories to look for templates.
* **template_module**: A python module to look for templates.

**Example**

.. code-block:: python

    from cement import App

    class MyApp(App):
        class Meta:
            label = 'myapp'
            extensions = ['generate', 'jinja2']
            template_handler = 'jinja2'


    with MyApp() as app:
        app.run()


Looks like:

.. code-block:: console

    $ python myapp.py --help
    usage: myapp [-h] [--debug] [--quiet] {generate} ...

    optional arguments:
      -h, --help  show this help message and exit
      --debug     toggle debug output
      --quiet     suppress all output

    sub-commands:
      {generate}
        generate  generate controller


    $ python myapp.py generate --help
    usage: myapp generate [-h] {plugin} ...

    optional arguments:
      -h, --help  show this help message and exit

    sub-commands:
      {plugin}
        plugin      generate plugin from template


**Generate Templates**

The Generate Extension looks for a ``generate`` sub-directory in all defined
template directory paths defined at the application level.  If it finds a
``generate`` directory it treats all items within that directory as a
generate template.

A Generate Template requires a single configuration YAML file called
``.generate.yml`` that looks something like:

.. code-block:: yaml

    ---

    ignore:
        - "^(.*)ignore-this(.*)$"
        - "^(.*)ignore-that(.*)$"

    exclude:
        - "^(.*)exclude-this(.*)$"
        - "^(.*)exclude-that(.*)$"

    variables:
        - name: 'my_variable_name'
          prompt: 'The Prompt Displayed to The User'

**Generate Template Configuration**

The following configurations are supported in a generate template's config:

* **ignore**: A list of regular expressions to match files that you want to
  completely ignore.
* **exclude**: A list of regular expressions to match files that you want to
  copy, but not render as a template.
* **variables**: A list of variable definitions that support the following
  sub-keys:
    * **name** *(required)*: The variable name (how it will be used in the
      template).
    * **prompt** *(required)*: The text displayed to the user to prompt for the
      value of ``name``.
    * **validate**: A single regular expression to validate the input value
      with.
    * **case**: A case modifyer to apply to the input value.  Valid options
      are: ``lower``, ``upper``, ``title``.
"""

import re
import os
import inspect
import yaml
from .. import Controller, minimal_logger, shell, FrameworkError

LOG = minimal_logger(__name__)


class GenerateTemplateAbstractBase(Controller):
    class Meta:
        pass

    def _default(self):
        source = self._meta.source_path
        dest = self.app.pargs.dest
        msg = 'Generating %s %s in %s' % (
                   self.app._meta.label, self._meta.label, dest
               )
        self.app.log.info(msg)
        data = {}

        f = open(os.path.join(source, '.generate.yml'))
        g_config = yaml.load(f)
        f.close()

        vars = g_config.get('variables', {})
        exclude_list = g_config.get('exclude', [])
        ignore_list = g_config.get('ignore', [])

        # default ignore the .generate.yml config
        g_config_yml = '^(.*)[\/\\\\]%s[\/\\\\]\.generate\.yml$' % \
                       self._meta.label
        ignore_list.append(g_config_yml)

        var_defaults = {
            'name': None,
            'prompt': None,
            'validate': None,
            'case': None,
            'default': None,
        }

        for defined_var in vars:
            var = var_defaults.copy()
            var.update(defined_var)
            for key in ['name', 'prompt']:
                assert var[key] is not None, \
                    "Required generate config key missing: %s" % key

            val = None
            if var['default'] is not None and self.app.pargs.defaults:
                val = var['default']

            elif 'default' is not None:
                default_text = ' [%s]' % var['default']

            else:
                default_text = ''

            if val is None:
                class MyPrompt(shell.Prompt):
                    class Meta:
                        text = "%s%s:" % (var['prompt'], default_text)
                        default = var.get('default', None)

                p = MyPrompt()
                val = p.prompt()

            if var['case'] in ['lower', 'upper', 'title']:
                val = getattr(val, var['case'])()
            elif var['case'] is not None:
                self.app.log.warning(
                    "Invalid configuration for variable " +
                    "'%s': " % var['name'] +
                    "case must be one of lower, upper, or title."
                )

            if var['validate'] is not None:
                assert re.match(var['validate'], val), \
                    "Invalid Response (must match: '%s')" % var['validate']

            data[var['name']] = val

        try:
            self.app.template.copy(source, dest, data,
                                   force=self.app.pargs.force,
                                   ignore=ignore_list,
                                   exclude=exclude_list)
        except AssertionError as e:
            if re.match('(.*)already exists(.*)', e.args[0]):
                raise AssertionError(e.args[0] + ' (try: --force)')
            else:
                raise


def setup_template_items(app):
    template_dirs = []
    template_items = []

    # nothing will work without a base controller
    try:
        assert app._meta.base_controller is not None, \
            "The ext.generate extension requires an application base " + \
            "controller, but none is defined!"
    except AssertionError as e:
        raise FrameworkError(e.args[0])

    # look in app template dirs
    for path in app._meta.template_dirs:
        subdir_path = os.path.join(path, 'generate')
        if os.path.exists(subdir_path):
            template_dirs.append(subdir_path)

    # use app template module, find it's path on filesystem
    if app._meta.template_module is not None:
        mod_parts = app._meta.template_module.split('.')
        mod = mod_parts.pop()
        try:
            mod = app.__import__(mod, from_module='.'.join(mod_parts))
            mod_path = os.path.dirname(inspect.getfile(mod))
            subdir_path = os.path.join(mod_path, 'generate')
            if os.path.exists(subdir_path):
                template_dirs.append(subdir_path)
        except AttributeError as e:
            msg = 'unable to load template module' + \
                  '%s from %s' % (mod, '.'.join(mod_parts))
            app.log.debug(msg)

    for path in template_dirs:
        for item in os.listdir(path):
            if item not in template_items:
                template_items.append(item)

            class GenerateTemplate(GenerateTemplateAbstractBase):
                class Meta:
                    label = item
                    stacked_on = 'generate'
                    stacked_type = 'nested'
                    help = 'generate %s from template' % item
                    arguments = [
                        # ------------------------------------------------------
                        (['dest'],
                         {'help': 'destination directory path'}),
                        # ------------------------------------------------------
                        (['-f', '--force'],
                         {'help': 'force operation if destination exists',
                          'dest': 'force',
                          'action': 'store_true'}),
                        # ------------------------------------------------------
                        (['-D', '--defaults'],
                         {'help': 'use all default variable values',
                          'dest': 'defaults',
                          'action': 'store_true'}),
                    ]
                    source_path = os.path.join(path, item)

            app.handler.register(GenerateTemplate)


class Generate(Controller):
    class Meta:
        label = 'generate'
        stacked_on = 'base'
        stacked_type = 'nested'
        config_section = 'generate'

    def _setup(self, app):
        super(Generate, self)._setup(app)

    def _default(self):
        self._parser.print_help()


def load(app):
    app.handler.register(Generate)
    app.hook.register('pre_run', setup_template_items)
