"""
Cement generate extension module.
"""

import re
import os
import inspect
import yaml
import shutil
from .. import Controller, minimal_logger, shell
from ..utils.version import VERSION, get_version

LOG = minimal_logger(__name__)


class GenerateTemplateAbstractBase(Controller):
    class Meta:
        pass

    def _generate(self, source, dest):
        from datetime import datetime
        from cement.utils.misc import pyid
        msg = 'Generating %s %s in %s' % (
                   self.app._meta.label, self._meta.label, dest
               )
        self.app.log.info(msg)

        # builtin vars
        maj_min = float('%s.%s' % (VERSION[0], VERSION[1]))
        today = datetime.today()
        dest_tail = os.path.split(dest.strip(os.path.sep))[-1].strip()
        data = dict(
            cement=dict(
                version=get_version(),
                major_version=VERSION[0],
                minor_version=VERSION[1],
                major_minor_version=maj_min,
            ),
            today=today,
            iso_today=today.date().isoformat(),
            dest_tail=dest_tail,
            dest_label=pyid(dest_tail, sep='_'),
        )

        f = open(os.path.join(source, '.generate.yml'))
        yaml_load = yaml.full_load if hasattr(yaml, 'full_load') else yaml.load
        g_config = yaml_load(f)
        f.close()

        vars = g_config.get('variables', {})
        exclude_list = g_config.get('exclude', [])
        ignore_list = g_config.get('ignore', [])

        # default ignore the .generate.yml config
        g_config_yml = r'^(.*)[\/\\\\]%s[\/\\\\]\.generate\.yml$' % \
                       self._meta.label
        ignore_list.append(g_config_yml)

        for var in vars:
            var_name = var.get('name', None)
            assert var_name is not None, \
                "Required generate config key missing: name"
            var_prompt = var.get('prompt', None)
            var_default = var.get('default', None)
            val = None
            if var_default is not None:
                var_default = self.__render(var_default, data)
                if self.app.pargs.defaults or var_prompt is None:
                    val = var_default

            if val is None:
                val = self.__prompt(var_prompt, var_default)
                val = self.__render(val, data)

            var_case = var.get('case', None)
            if var_case in ['lower', 'upper', 'title']:
                val = getattr(val, var_case)()
            elif var_case is not None:
                self.app.log.warning(
                    "Invalid configuration for variable " +
                    "'%s': " % var_name +
                    "case must be one of lower, upper, or title."
                )

            var_validate = var.get('validate', None)
            if var_validate is not None:
                assert re.match(var_validate, val), \
                    "Invalid Response (must match: '%s')" % var_validate

            data[var_name] = val

        try:
            self.app.template.copy(source, dest, data,
                                   force=self.app.pargs.force,
                                   ignore=ignore_list,
                                   exclude=exclude_list)
        except AssertionError as e:
            if re.match('(.*)already exists(.*)', e.args[0]):
                raise AssertionError(e.args[0] + ' (try: --force)')
            else:
                raise  # pragma: nocover

    def _clone(self, source, dest):
        msg = 'Cloning %s %s template to %s' % (
                   self.app._meta.label, self._meta.label, dest
               )
        self.app.log.info(msg)

        if os.path.exists(dest) and self.app.pargs.force is True:
            shutil.rmtree(dest)
        elif os.path.exists(dest):
            msg = "Destination path already exists: %s (try: --force)" % dest
            raise AssertionError(msg)

        shutil.copytree(source, dest)

    def _default(self):
        source = self._meta.source_path
        dest = self.app.pargs.dest

        if self.app.pargs.clone is True:
            self._clone(source, dest)
        else:
            self._generate(source, dest)

    @staticmethod
    def __prompt(prompt, var_default):
        if prompt is not None:
            default_text = ' [%s]' % var_default if var_default else ''

            class MyPrompt(shell.Prompt):
                class Meta:
                    text = "%s%s:" % (prompt, default_text)
                    default = var_default

            p = MyPrompt()
            return p.prompt()    # pragma: nocover
        else:
            assert var_default is not None, \
                "Required generate config key missing: prompt"
            return var_default

    def __render(self, value, data):
        if '{{' in value:
            value = self.app.template.render(value, data)
        return value


def setup_template_items(app):
    template_dirs = []
    template_items = []

    # look in app template dirs
    for path in app._meta.template_dirs:
        subpath = os.path.join(path, 'generate')
        if os.path.exists(subpath) and subpath not in template_dirs:
            template_dirs.append(subpath)

    # use app template module, find it's path on filesystem
    if app._meta.template_module is not None:
        mod_parts = app._meta.template_module.split('.')
        mod = mod_parts.pop()
        try:
            mod = app.__import__(mod, from_module='.'.join(mod_parts))
            mod_path = os.path.dirname(inspect.getfile(mod))
            subpath = os.path.join(mod_path, 'generate')

            if os.path.exists(subpath) and subpath not in template_dirs:
                template_dirs.append(subpath)

        # FIXME: not exactly sure how to test for this so not covering
        except AttributeError:                                # pragma: nocover
            msg = 'unable to load template module' + \
                  '%s from %s' % (mod, '.'.join(mod_parts))   # pragma: nocover
            app.log.debug(msg)                                # pragma: nocover

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
                        # ------------------------------------------------------
                        (['--clone'],
                         {'help': 'clone this template to destination path',
                          'dest': 'clone',
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
