"""
Cement generate extension module.
"""

import inspect
import os
import re
import shutil
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import yaml  # type: ignore

from .. import Controller, minimal_logger, shell
from ..utils.version import VERSION, get_version

if TYPE_CHECKING:
    from ..core.foundation import App  # pragma: nocover  # TYPE_CHECKING import

LOG = minimal_logger(__name__)


class GenerateTemplateAbstractBase(Controller):
    class Meta(Controller.Meta):
        pass

    _meta: Meta  # type: ignore

    def _process_features(self,
                          features: list[dict[str, Any]],
                          vars: list[dict[str, Any]],
                          exclude_list: list[str],
                          ignore_list: list[str],
                          data: dict[str, Any]) -> None:
        # validate up front so misconfigurations fail fast and consistently
        # under `python -O` (asserts get stripped, ValueError does not).
        feature_by_name: dict[str, dict[str, Any]] = {}
        for feature in features:
            if feature.get('name') is None:
                raise ValueError(
                    "Required feature config key missing: name")
            feature_by_name[feature['name']] = feature
        for feature in features:
            for req in feature.get('requires', []):
                if req not in feature_by_name:
                    raise ValueError(
                        f"Feature '{feature['name']}' requires unknown "
                        f"feature '{req}'")

        # Resolve features lazily and recursively so that:
        #   1. resolution is order-independent — a feature may declare
        #      `requires` against another feature defined later in the YAML;
        #   2. interactive runs do not nag the user for a feature whose
        #      `requires` already resolved to False (the prompt is reached
        #      only after every prerequisite returned True).
        feature_states: dict[str, bool] = {}

        def _resolve(name: str) -> bool:
            if name in feature_states:
                return feature_states[name]
            feature = feature_by_name[name]
            for req in feature.get('requires', []):
                if not _resolve(req):
                    self.app.log.warning(
                        f"Feature '{name}' disabled (requires: {req})"
                    )
                    feature_states[name] = False
                    return False
            default = bool(feature.get('default', False))
            if self.app.pargs.defaults:
                feature_states[name] = default
            else:
                default_hint = 'Y/n' if default else 'y/N'  # pragma: nocover
                default_val = 'y' if default else 'n'  # pragma: nocover

                class FeaturePrompt(shell.Prompt):  # pragma: nocover
                    class Meta:
                        text = f"Enable Feature: {name} [{default_hint}]:"
                        default = default_val

                p = FeaturePrompt(auto=False)  # pragma: nocover
                val: str = p.prompt() or default_val  # pragma: nocover
                feature_states[name] = val.lower() == 'y'  # pragma: nocover
            return feature_states[name]

        for feature in features:
            _resolve(feature['name'])

        # merge enabled/disabled configs
        if 'features' not in data:
            data['features'] = {}
        for feature in features:
            name = feature['name']
            enabled = feature_states[name]
            data['features'][name] = enabled

            block_key = 'enabled' if enabled else 'disabled'
            block = feature.get(block_key) or {}

            vars.extend(block.get('variables', []))
            exclude_list.extend(block.get('exclude', []))
            ignore_list.extend(block.get('ignore', []))

    def _generate(self, source: str, dest: str) -> None:
        msg = f'Generating {self.app._meta.label} {self._meta.label} in {dest}'
        self.app.log.info(msg)
        data: dict[str, dict[str, Any]] = {}

        # builtin vars
        maj_min = float(f'{VERSION[0]}.{VERSION[1]}')
        data['cement'] = {}
        data['cement']['version'] = get_version()
        data['cement']['major_version'] = VERSION[0]
        data['cement']['minor_version'] = VERSION[1]
        data['cement']['major_minor_version'] = maj_min

        f = open(os.path.join(source, '.generate.yml'))
        yaml_load: Callable = yaml.full_load if hasattr(yaml, 'full_load') else yaml.load
        g_config = yaml_load(f)
        f.close()

        # Use `or []` (not the .get default) so explicit `key: null` in the
        # YAML coalesces to an empty list — otherwise the subsequent
        # `for ... in vars` / `ignore_list.append(...)` would crash on None.
        vars = g_config.get('variables') or []
        exclude_list = g_config.get('exclude') or []
        ignore_list = g_config.get('ignore') or []

        # default ignore the .generate.yml config
        g_config_yml = rf'^(.*)[\/\\\\]{self._meta.label}[\/\\\\]\.generate\.yml$'
        ignore_list.append(g_config_yml)

        # process features (merge enabled/disabled config into vars/exclude/ignore)
        features = g_config.get('features', [])
        if features:
            self._process_features(features, vars, exclude_list,
                                   ignore_list, data)

        var_defaults: dict = {
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
                    f"Required generate config key missing: {key}"

            val: Any = None
            if var['default'] is not None and self.app.pargs.defaults:
                val = var['default']

            elif var['default'] is not None:
                default_text = f" [{var['default']}]"

            else:
                default_text = ''   # pragma: nocover  # defensive: unreachable

            if val is None:
                class MyPrompt(shell.Prompt):
                    class Meta:
                        text = f"{var['prompt']}{default_text}:"
                        default = var.get('default', None)

                p = MyPrompt()
                val = p.prompt()    # pragma: nocover  # defensive: unreachable

            if var['case'] in ['lower', 'upper', 'title']:
                val = getattr(val, var['case'])()
            elif var['case'] is not None:
                self.app.log.warning(
                    "Invalid configuration for variable " +
                    f"'{var['name']}': " +
                    "case must be one of lower, upper, or title."
                )

            if var['validate'] is not None:
                assert re.match(var['validate'], val), \
                    f"Invalid Response (must match: '{var['validate']}')"

            data[var['name']] = val

        try:
            self.app.template.copy(source, dest, data,
                                   force=self.app.pargs.force,
                                   ignore=ignore_list,
                                   exclude=exclude_list)
        except AssertionError as e:
            if re.match('(.*)already exists(.*)', e.args[0]):
                raise AssertionError(e.args[0] + ' (try: --force)') from e
            else:
                raise  # pragma: nocover  # defensive: unreachable

    def _clone(self, source: str, dest: str) -> None:
        msg = f'Cloning {self.app._meta.label} {self._meta.label} template to {dest}'
        self.app.log.info(msg)

        if os.path.exists(dest) and self.app.pargs.force is True:
            shutil.rmtree(dest)
        elif os.path.exists(dest):
            msg = f"Destination path already exists: {dest} (try: --force)"
            raise AssertionError(msg)

        shutil.copytree(source, dest)

    def _default(self) -> None:
        source = self._meta.source_path
        dest = self.app.pargs.dest

        if self.app.pargs.clone is True:
            self._clone(source, dest)
        else:
            self._generate(source, dest)


def setup_template_items(app: "App") -> None:
    template_dirs = []
    template_items = []

    # look in app template dirs
    for path in app._meta.template_dirs:
        subpath = os.path.join(path, 'generate')
        if os.path.exists(subpath) and subpath not in template_dirs:
            template_dirs.append(subpath)

    # use app template module, find its path on filesystem
    if app._meta.template_module is not None:
        mod_parts = app._meta.template_module.split('.')
        mod_name = mod_parts.pop()
        try:
            mod = app.__import__(mod_name, from_module='.'.join(mod_parts))
            mod_path = os.path.dirname(inspect.getfile(mod))
            subpath = os.path.join(mod_path, 'generate')

            if os.path.exists(subpath) and subpath not in template_dirs:
                template_dirs.append(subpath)

        # FIXME: AttributeError can fire if the imported module lacks
        # __file__ (e.g., built-in / namespace packages); not testable
        # from cement, so keep pragma: nocover on this branch.
        except AttributeError:  # pragma: nocover  # untestable: dynamic import
            msg = ('unable to load template module '
                   f"'{mod_name}' from '{'.'.join(mod_parts)}'")
            app.log.debug(msg)  # pragma: nocover  # untestable: dynamic import
        except ModuleNotFoundError as e:
            # Only swallow when the missing module is the template module
            # path we tried to import. A ModuleNotFoundError raised inside
            # the user's template module (transitive dep missing) must
            # propagate — otherwise we mask the real failure as a generic
            # "template module not found" debug log.
            expected = '.'.join(mod_parts + [mod_name])
            if e.name and e.name != expected and \
                    not expected.startswith(f"{e.name}."):
                raise
            msg = ('unable to load template module '
                   f"'{mod_name}' from '{'.'.join(mod_parts)}'")
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
                    help = f'generate {item} from template'
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
    class Meta(Controller.Meta):
        label = 'generate'
        stacked_on = 'base'
        stacked_type = 'nested'
        config_section = 'generate'

    _meta: Meta  # type: ignore

    def _setup(self, app: "App") -> None:
        super()._setup(app)

    def _default(self) -> None:
        self._parser.print_help()


def load(app: "App") -> None:
    app.handler.register(Generate)
    app.hook.register('pre_run', setup_template_items)
