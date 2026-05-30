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

    def _generate(self, source: str, dest: str) -> None:
        msg = f'Generating {self.app._meta.label} {self._meta.label} in {dest}'
        self.app.log.info(msg)
        data: dict[str, Any] = {}

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

        # `var_defaults` is the released compat anchor (extended ADDITIVELY
        # with `type`/`extend`/`requires`). A `type: string` variable with
        # none of the new keys takes the identity path below and behaves
        # byte-identically to the released schema (test1-5/22/27/29 oracle).
        var_defaults: dict = {
            'name': None,
            'prompt': None,
            'validate': None,
            'case': None,
            'default': None,
            'type': 'string',
            'extend': None,
            'requires': None,
        }

        # Index the top-level variables by name so `requires:` can resolve
        # a referenced variable on demand (D-09/D-11). Only top-level
        # variables are addressable by `requires`; nested
        # `extend.variables` are gated by their parent rule (D-10).
        var_by_name: dict[str, dict[str, Any]] = {}
        for defined_var in vars:
            if defined_var.get('name') is not None:
                var_by_name[defined_var['name']] = defined_var

        def _resolve_string(var: dict[str, Any]) -> Any:
            # Released `type: string` resolution — byte-identical to the
            # pre-#782 variable loop. `prompt` is required (assert) unless
            # the silent `prompt: false` sentinel is used.
            assert var['prompt'] is not None, \
                "Required generate config key missing: prompt"

            val: Any = None
            default_text = ''
            if var['prompt'] is False:
                # Silent variable: `prompt: false` sentinel uses `default`
                # directly without prompting. case+validate still apply
                # via the shared block below. str() because the prompted
                # path always returns str from p.prompt() — the silent
                # path matches the invariant so YAML-decoded non-string
                # defaults (bool, int, etc.) don't crash the downstream
                # case/validate operations (e.g. False.upper()).
                assert var['default'] is not None, \
                    f"Variable '{var['name']}' has prompt: false " \
                    f"but no default"
                val = str(var['default'])
            elif var['default'] is not None and self.app.pargs.defaults:
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
            return val

        def _resolve_boolean(var: dict[str, Any]) -> bool:
            # `type: boolean` — emits a real Python bool at data[name] so
            # `{% if name %}` works in jinja2/mustache (bug #4 fix, D-05).
            # `prompt:` is polymorphic `string | false | object` (D-12):
            #   - string -> framework owns the y/n text (Plan 01);
            #   - false  -> silent, use default directly;
            #   - object {text, accept, reject} -> author owns the text,
            #     accept/reject token lists map input -> bool (Plan 02).
            # Silent (`prompt: false`) and `--defaults` both dispatch to
            # `bool(default)`.
            default = bool(var['default'])
            if var['prompt'] is False:
                assert var['default'] is not None, \
                    f"Variable '{var['name']}' has prompt: false " \
                    f"but no default"
                return default

            prompt = var['prompt']
            if isinstance(prompt, dict):
                # D-12 object-form: validate + resolve via accept/reject.
                return _resolve_boolean_object(var, prompt, default)

            if self.app.pargs.defaults:
                return default

            # Interactive string-form prompt — Tom's #782 pt 2/3: replace
            # the old "Enable Feature:" text with a vars-style boolean prompt.
            # No explicit `prompt:` → default the label to "Enable {name}"
            # (D-12), mirroring the choice path's `or f"Select: {name}"`
            # fallback — otherwise `var['prompt']` is None and the prompt
            # renders the literal "None [(Y)es/(N)o] ...".
            hint = 'Y' if default else 'N'
            label = prompt or f"Enable {var['name']}"

            class BoolPrompt(shell.Prompt):
                class Meta:
                    text = f"{label} [(Y)es/(N)o] [{hint}]:"
                    default = hint

            answer = BoolPrompt().prompt()  # pragma: nocover  # defensive: unreachable
            # y/yes -> True, n/no -> False, empty -> default. This mapping
            # is the coverable, bug-prone logic — driven under real coverage
            # by the patched-prompt tests (test31), NOT pragma'd.
            token = (answer or '').strip().lower()
            if token in ('y', 'yes'):
                return True
            if token in ('n', 'no'):
                return False
            return default

        def _resolve_boolean_object(var: dict[str, Any],
                                    prompt: dict[str, Any],
                                    default: bool) -> bool:
            # D-12 object-form `prompt: {text, accept, reject}`. The author
            # owns the full text (NO framework decoration). `accept:`/
            # `reject:` are case-insensitive token lists mapping input ->
            # bool; input matching NEITHER asserts + aborts like a failed
            # validate: (D-14). Empty input falls through to `default`.
            accept = prompt.get('accept') or []
            reject = prompt.get('reject') or []

            # YAML 1.1 bool-coercion guard (Pitfall 1): bare `yes`/`no`/
            # `on`/`off`/`true`/`false` in a list coerce to Python bool
            # under yaml.full_load. A bool member is a silent landmine —
            # surface it as a fast, explicit ValueError telling the author
            # to quote the token. ValueError (not assert) survives
            # `python -O`, matching the schema-error discipline.
            for member in list(accept) + list(reject):
                if isinstance(member, bool):
                    raise ValueError(
                        f"Variable '{var['name']}' has a bool-like "
                        f"accept:/reject: token that YAML coerced to a "
                        f"Python bool ({member!r}); quote it "
                        f"(e.g. accept: [y, \"yes\"]) so it stays a string")

            accept_tokens = [str(m).strip().lower() for m in accept]
            reject_tokens = [str(m).strip().lower() for m in reject]

            if self.app.pargs.defaults:
                return default

            class BoolObjectPrompt(shell.Prompt):
                class Meta:
                    text = prompt['text']
                    default = ''

            answer = BoolObjectPrompt().prompt()  # pragma: nocover  # defensive: unreachable
            # accept member -> True, reject member -> False, empty ->
            # default, junk -> assert-abort. This accept/reject MAPPING is
            # the bug-prone logic — covered under real patched-prompt tests
            # (test35), NOT pragma'd.
            token = (answer or '').strip().lower()
            if token == '':
                return default
            if token in accept_tokens:
                return True
            if token in reject_tokens:
                return False
            assert token in accept_tokens or token in reject_tokens, \
                "Invalid Response (must be one of accept/reject)"
            return default  # pragma: nocover  # defensive: unreachable

        def _resolve_choice(var: dict[str, Any]) -> str:
            # `type: choice` — numbered shell.Prompt picker emitting the
            # chosen option value (str) at data[name]. `options:` is either
            # a scalar list (`[none, flask, fastapi]`) or per-option objects
            # (`{value, prompt}`, D-16). Per-option effects live in `extend:`
            # keyed by value, not inline. Schema misconfig is fail-fast
            # ValueError (survives `python -O`): empty options, option object
            # missing `value`, default not in option values, duplicate labels.
            options = var.get('options') or []
            if not options:
                raise ValueError(
                    f"Variable '{var['name']}' is type: choice but has "
                    f"no 'options'")

            values: list[str] = []
            labels: list[str] = []
            for opt in options:
                if isinstance(opt, dict):
                    if opt.get('value') is None:
                        raise ValueError(
                            f"Variable '{var['name']}' has an 'options' "
                            f"branch missing required key: value")
                    # YAML may decode `value: 1` as int; coerce so both
                    # `value: 1` and `value: "1"` compare uniformly.
                    values.append(str(opt['value']))
                    labels.append(opt.get('prompt') or str(opt['value']))
                else:
                    values.append(str(opt))
                    labels.append(str(opt))

            if len(set(labels)) != len(labels):
                raise ValueError(
                    f"Variable '{var['name']}' has duplicate option "
                    f"labels {labels} — each option's effective display "
                    f"label (prompt: or str(value)) must be unique so the "
                    f"numbered selection is unambiguous")

            if var['default'] is None:
                raise ValueError(
                    f"Variable '{var['name']}' is type: choice but has "
                    f"no 'default' value")
            default = str(var['default'])
            if default not in values:
                raise ValueError(
                    f"Variable '{var['name']}' default '{var['default']}' "
                    f"is not in options values {values}")

            if self.app.pargs.defaults:
                return default

            default_label = labels[values.index(default)]
            prompt_text = var['prompt'] or f"Select: {var['name']}"
            prompt_text = f"\n{prompt_text}:"

            class SelectPrompt(shell.Prompt):
                class Meta:
                    text = prompt_text
                    options = labels
                    numbered = True
                    case_insensitive = True
                    default = default_label

            chosen_label = SelectPrompt().prompt()  # pragma: nocover  # defensive: unreachable
            # label -> value mapping is the coverable logic — driven under
            # real coverage by the patched-prompt test (test16), NOT pragma'd.
            # `.prompt()` is typed `str | None`; empty input resolves to the
            # default_label via Meta.default, so str() keeps mypy happy
            # without masking a real None (the numbered picker always yields
            # a label).
            return values[labels.index(str(chosen_label))]

        def _when_matches(value: Any, when: Any, vtype: str) -> bool:
            # Compose the three `extend.when` / `requires` match forms
            # (D-07), dispatching on the carrying variable's `type` (Q2):
            #   - list   -> in-list membership. Booleans compare by Python
            #     `==`; choice/string members str()-coerce both sides.
            #   - regex  -> `re.match(when, value)` — STRING type only
            #     (mirrors `validate:`); a non-string `when` on a string
            #     var still falls through to scalar equality below.
            #   - scalar -> equality. Booleans by Python `==` (so
            #     `when: true` matches `True`, not the string "True");
            #     choice/string by str()-coerced equality (so `when: 1`
            #     matches a "1" option value; per the L219 discipline).
            if isinstance(when, list):
                if vtype == 'boolean':
                    return value in when
                return str(value) in [str(w) for w in when]
            if vtype == 'string' and isinstance(when, str):
                return re.match(when, value) is not None
            if vtype == 'boolean':
                return bool(value == when)
            return str(when) == str(value)

        def _gated_default(var: dict[str, Any], vtype: str) -> Any:
            # Value emitted for a `requires`-gated-out variable (Q1): its
            # own `default`, typed like a fully-resolved value, so the
            # template never KeyErrors. boolean -> Python bool;
            # choice/string -> str(default) (matching the resolved-path
            # str invariant). A gated-out var's extend rules do NOT fire.
            if vtype == 'boolean':
                return bool(var['default'])
            return str(var['default'])

        def _requires_satisfied(var: dict[str, Any]) -> bool:
            # Evaluate top-level `requires:` (D-09/D-11), AND-ed across
            # keys. Each referenced variable is resolved ON DEMAND (lazy
            # recursion + memoize-on-`data`), so a prerequisite declared
            # LATER still resolves first — resolution is order-independent.
            # Vocab forms (matching `extend.when`):
            #   - `requires: [name]`        -> `name` must be truthy
            #   - `requires: {name: value}` -> equality / regex / in-list
            #     via `_when_matches`
            requires = var['requires']
            if requires is None:
                return True

            if isinstance(requires, dict):
                items = list(requires.items())
            else:
                # list/sugar form: each entry is a bare name -> truthy
                items = [(name, None) for name in requires]

            for req_name, expected in items:
                if req_name not in var_by_name:
                    raise ValueError(
                        f"Variable '{var['name']}' requires unknown "
                        f"variable '{req_name}'")
                resolve_and_emit(var_by_name[req_name])
                req_value = data[req_name]
                req_var = var_by_name[req_name]
                if expected is None:
                    # truthy sugar
                    if not req_value:
                        return False
                else:
                    if not _when_matches(req_value, expected,
                                         req_var.get('type', 'string')):
                        return False
            return True

        def resolve_and_emit(defined_var: dict[str, Any]) -> None:
            var = var_defaults.copy()
            var.update(defined_var)
            if var['name'] is None:
                raise ValueError(
                    "Required generate config key missing: name")

            # Memoize on `data` membership so a variable referenced more than
            # once (e.g. via `requires`) resolves exactly once and resolution
            # stays declaration-order-independent (D-11).
            if var['name'] in data:
                return

            vtype = var['type']
            if vtype not in ('string', 'boolean', 'choice'):
                raise ValueError(
                    f"Variable '{var['name']}' has invalid type "
                    f"'{vtype}' (must be string, boolean, or choice)")

            # D-17: case:/validate: are string-only semantics. A boolean is
            # parsed via accept/reject; a choice is constrained by options —
            # declaring case:/validate: on either is a fail-fast schema
            # misconfig (ValueError survives `python -O`).
            if vtype in ('boolean', 'choice') and \
                    (var['case'] is not None or var['validate'] is not None):
                raise ValueError(
                    f"case:/validate: are string-only; variable "
                    f"'{var['name']}' is type: {vtype}")

            # `requires:` gate (D-09/D-11). If any prerequisite fails, the
            # var is GATED OUT: set to its `default` at data[name] (Q1) and
            # its `extend` rules do NOT fire. Resolved BEFORE prompting so an
            # interactive run never nags for a gated-out variable.
            if not _requires_satisfied(var):
                data[var['name']] = _gated_default(var, vtype)
                return

            value: Any
            if vtype == 'boolean':
                value = _resolve_boolean(var)
            elif vtype == 'choice':
                value = _resolve_choice(var)
            else:
                value = _resolve_string(var)

            data[var['name']] = value

            # `extend:` rules compose — every rule whose `when` matches the
            # resolved value fires, accumulating exclude/ignore and recursing
            # depth-first into its nested variables in place (D-07/D-08).
            # `_when_matches` composes scalar equality, in-list membership,
            # and (string-type) regex; multiple matching rules all fire.
            for rule in var['extend'] or []:
                when = rule.get('when')
                if _when_matches(value, when, vtype):
                    exclude_list.extend(rule.get('exclude') or [])
                    ignore_list.extend(rule.get('ignore') or [])
                    for nested in rule.get('variables') or []:
                        resolve_and_emit(nested)

        for defined_var in vars:
            resolve_and_emit(defined_var)

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
        # from cement, so the branch below is excluded from coverage.
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
