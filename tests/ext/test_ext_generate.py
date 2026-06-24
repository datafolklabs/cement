import os
import re
from unittest.mock import patch

from cement import Controller, TestApp
from cement.utils import shell
from cement.utils.test import raises


def exists_join(*paths):
    return os.path.exists(os.path.join(*paths))


class GenerateBase(Controller):
    class Meta:
        label = 'base'


class GenerateApp(TestApp):
    class Meta:
        extensions = ['jinja2', 'yaml', 'generate', 'alarm']
        template_handler = 'jinja2'
        template_module = 'tests.data.templates'
        handlers = [GenerateBase]


def test_generate(tmp):
    argv = ['generate', 'test1', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        app.run()

        # should have everything
        assert exists_join(tmp.dir, 'take-me')
        res = open(os.path.join(tmp.dir, 'take-me')).read()
        assert res.find('bar1') >= 0
        assert res.find('bar2') >= 0
        assert res.find('BAR3') >= 0
        assert res.find('Bar4') >= 0
        assert res.find('bar5') >= 0
        assert res.find('bar6') >= 0

        # copied but not rendered
        assert exists_join(tmp.dir, 'exclude-me')
        res = open(os.path.join(tmp.dir, 'exclude-me')).read()
        assert re.match(r'.*foo1 => \{\{ foo1 \}\}.*', res)

        # should not have been copied
        assert not exists_join(tmp.dir, 'ignore-me')

    # test generate again to trigger already exists

    with GenerateApp(argv=argv) as app:
        with raises(AssertionError, match='Destination file already exists'):
            app.run()


def test_prompt(tmp):
    argv = ['generate', 'test1', tmp.dir]

    with GenerateApp(argv=argv) as app:
        msg = "reading from stdin while output is captured"
        with raises(OSError, match=msg):
            app.run()


def test_invalid_case(tmp):
    argv = ['generate', 'test3', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        app.run()

        assert exists_join(tmp.dir, 'take-me')
        with open(os.path.join(tmp.dir, 'take-me')) as f:
            res = f.read()
            # Assert that the case was not modified
            assert 'bar1' in res


def test_invalid_variable_value(tmp):
    argv = ['generate', 'test2', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        msg = "Invalid Response.*"
        with raises(AssertionError, match=msg):
            app.run()


def test_no_default(tmp):
    with patch.object(shell.Prompt, 'prompt', return_value='Bogus'):
        argv = ['generate', 'test5', tmp.dir]

        with GenerateApp(argv=argv) as app:
            app.run()
            with open(os.path.join(tmp.dir, 'take-me')) as f:
                res = f.read()
                assert 'Bogus' in res


def test_clone(tmp):
    # first test for already exists
    argv = ['generate', 'test1', '--clone', tmp.dir]
    with raises(AssertionError, match='(.*)already exists(.*)'):
        with GenerateApp(argv=argv) as app:
            app.run()

    # then force it
    argv = ['generate', 'test1', '--clone', tmp.dir, '--force']
    with GenerateApp(argv=argv) as app:
        app.run()

    assert exists_join(tmp.dir, '.generate.yml')


def test_generate_from_template_dir(tmp):
    class NoTemplateApp(TestApp):
        class Meta:
            extensions = ['jinja2', 'yaml', 'generate', 'alarm']
            template_handler = 'jinja2'
            template_module = __name__
            handlers = [GenerateBase]

    # should use the templates dir passed as keyword
    # instead of the template_module in the Meta info
    argv = ['generate', 'test1', tmp.dir, '--defaults']
    with NoTemplateApp(argv=argv, template_dir='tests/data/templates') as app:
        app.run()

        assert exists_join(tmp.dir, 'take-me')
        res = open(os.path.join(tmp.dir, 'take-me')).read()
        assert res.find('bar1') >= 0


def test_generate_default_command(tmp):
    # default command for generate should call print_help
    patch_target = 'cement.ext.ext_argparse.ArgparseArgumentHandler.print_help'
    with patch(patch_target) as mock:
        argv = ['generate']
        with GenerateApp(argv=argv) as app:
            app.run()
    assert mock.call_count == 1


def test_filtered_sub_dirs(tmp):
    tmp.cleanup = False
    argv = ['generate', 'test4', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        app.run()

        assert exists_join(tmp.dir, 'take-me')
        assert exists_join(tmp.dir, 'take-me', 'take-me')
        assert exists_join(tmp.dir, 'take-me', 'exclude-me')
        assert not exists_join(tmp.dir, 'take-me', 'ignore-me')
        assert exists_join(tmp.dir, 'exclude-me')
        assert exists_join(tmp.dir, 'exclude-me', 'take-me')
        assert not exists_join(tmp.dir, 'ignore-me')
        assert not exists_join(tmp.dir, 'ignore-me', 'take-me')


def test_generate_features_enabled(tmp):
    # feature1 defaults to true, feature2 defaults to false
    argv = ['generate', 'test6', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        app.run()

        # base variable rendered
        assert exists_join(tmp.dir, 'take-me')
        with open(os.path.join(tmp.dir, 'take-me')) as f:
            res = f.read()
            assert 'myapp' in res

        # feature1 enabled: its variable is available and rendered
        assert exists_join(tmp.dir, 'feature1-file')
        with open(os.path.join(tmp.dir, 'feature1-file')) as f:
            res = f.read()
            assert 'feature1_val' in res

        # feature1 enabled: feature1-only is kept (not ignored)
        assert exists_join(tmp.dir, 'feature1-only')

        # feature1 enabled: no-feature1 is ignored
        assert not exists_join(tmp.dir, 'no-feature1')

        # feature2 disabled: feature2-only is ignored
        assert not exists_join(tmp.dir, 'feature2-only')


def test_generate_features_disabled(tmp):
    # test6 with feature1 disabled via a separate config (test7)
    # create test7 that flips defaults: feature1=false, feature2=true
    argv = ['generate', 'test7', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        app.run()

        # base variable rendered
        assert exists_join(tmp.dir, 'take-me')
        with open(os.path.join(tmp.dir, 'take-me')) as f:
            res = f.read()
            assert 'myapp' in res

        # feature1 disabled: feature1-file is excluded (copied, not rendered)
        assert exists_join(tmp.dir, 'feature1-file')
        with open(os.path.join(tmp.dir, 'feature1-file')) as f:
            res = f.read()
            assert re.match(r'.*\{\{ feature1_var \}\}.*', res)

        # feature1 disabled: feature1-only is ignored
        assert not exists_join(tmp.dir, 'feature1-only')

        # feature1 disabled: no-feature1 is kept
        assert exists_join(tmp.dir, 'no-feature1')

        # feature2 enabled: feature2-only is kept
        assert exists_join(tmp.dir, 'feature2-only')

        # feature2 enabled: its variable is available
        assert exists_join(tmp.dir, 'feature2-file')
        with open(os.path.join(tmp.dir, 'feature2-file')) as f:
            res = f.read()
            assert 'feature2_val' in res


def test_generate_features_missing_name(tmp):
    # test8: a variable missing the required `name` key → ValueError
    # (config schema error, fail-fast, survives `python -O`).
    argv = ['generate', 'test8', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        with raises(ValueError, match='Required generate config key missing: name'):
            app.run()


def test_generate_features_requires_satisfied(tmp):
    # test9: feature1=true (default), feature2=true (default) requires
    # feature1. Both gates pass, neither `when: false` ignore fires, so
    # both feature1-only and feature2-only stay.
    argv = ['generate', 'test9', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        app.run()

        # both features enabled, both files present
        assert exists_join(tmp.dir, 'take-me')
        assert exists_join(tmp.dir, 'feature1-only')
        assert exists_join(tmp.dir, 'feature2-only')


def test_generate_features_requires_not_satisfied(tmp):
    # test11: feature1=false (default) → its `when: false` ignores
    # feature1-only. feature2=true requires feature1, so feature2 is
    # GATED OUT: set to its default and its `when: true` extend rule does
    # NOT fire (Q1). feature2-only therefore STAYS (the gated-out var's
    # effects are omitted, not inverted into a disabled block).
    argv = ['generate', 'test11', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        app.run()

        assert exists_join(tmp.dir, 'take-me')

        # feature1 false: its when:false rule fires, feature1-only ignored
        assert not exists_join(tmp.dir, 'feature1-only')

        # feature2 gated out via requires: its extend rule does NOT fire,
        # so feature2-only is kept (Q1 — effects omitted, not disabled)
        assert exists_join(tmp.dir, 'feature2-only')


def test_generate_features_requires_unknown(tmp):
    # test10: a variable requires a nonexistent variable → ValueError.
    argv = ['generate', 'test10', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        with raises(ValueError, match="requires unknown variable"):
            app.run()


def test_generate_requires_gated_no_default(tmp):
    # test43: `dependent` (a string var) is gated out by `requires: feature1`
    # (feature1 defaults false) but declares no `default`. Emitting it would
    # otherwise leak the literal string "None" into the context; instead
    # _gated_default fail-fasts with a clear ValueError.
    argv = ['generate', 'test43', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        with raises(ValueError, match="requires: but has no default"):
            app.run()


def test_generate_requires_cycle(tmp):
    # test44: alpha requires beta and beta requires alpha — a dependency
    # cycle. resolve_and_emit's in-flight guard raises a clear ValueError
    # rather than recursing until Python raises RecursionError.
    argv = ['generate', 'test44', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        with raises(ValueError, match="Cyclic variable dependency"):
            app.run()


def test_generate_features_minimal(tmp):
    # test13: feature with only name and default, no enabled/disabled blocks
    argv = ['generate', 'test13', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        app.run()

        assert exists_join(tmp.dir, 'take-me')
        with open(os.path.join(tmp.dir, 'take-me')) as f:
            res = f.read()
            assert 'myapp' in res


def test_generate_boolean_prompt_yes(tmp):
    # test31: type: boolean with a string-form prompt, run interactively
    # (no --defaults). Patch shell.Prompt.prompt to return "yes" → the
    # y/yes→True mapping runs and data[name] is True (jinja renders the
    # enabled branch).
    with patch.object(shell.Prompt, 'prompt', return_value='yes'):
        argv = ['generate', 'test31', tmp.dir]
        with GenerateApp(argv=argv) as app:
            app.run()
            with open(os.path.join(tmp.dir, 'take-me')) as f:
                assert 'enabled' in f.read()


def test_generate_boolean_prompt_no(tmp):
    # test31: prompt returns "n" → n/no→False mapping; data[name] False.
    with patch.object(shell.Prompt, 'prompt', return_value='n'):
        argv = ['generate', 'test31', tmp.dir]
        with GenerateApp(argv=argv) as app:
            app.run()
            with open(os.path.join(tmp.dir, 'take-me')) as f:
                assert 'disabled' in f.read()


def test_generate_boolean_prompt_empty_uses_default(tmp):
    # test31: prompt returns "" (empty) → falls through to the var's bool
    # default (false) → data[name] False.
    with patch.object(shell.Prompt, 'prompt', return_value=''):
        argv = ['generate', 'test31', tmp.dir]
        with GenerateApp(argv=argv) as app:
            app.run()
            with open(os.path.join(tmp.dir, 'take-me')) as f:
                assert 'disabled' in f.read()


def test_generate_boolean_prompt_no_label_defaults_to_enable(tmp):
    # test42: type: boolean string-form with NO `prompt:` key. The
    # framework must default the label to "Enable {name}" (D-12) — the
    # rendered prompt text reads "Enable enable_thing [(Y)es/(N)o] [N]:",
    # NOT the literal "None [(Y)es/(N)o] [N]:". An explicit `prompt:` on
    # the second var ("Use Other") still wins. Capture each prompt's
    # bound Meta.text via a recorder patched onto shell.Prompt.prompt
    # (mirrors the test31 patched-prompt pattern), then assert the labels.
    seen = []

    def record(self):
        seen.append(self._meta.text)
        return ''

    with patch.object(shell.Prompt, 'prompt', record):
        argv = ['generate', 'test42', tmp.dir]
        with GenerateApp(argv=argv) as app:
            app.run()

    assert 'Enable enable_thing [(Y)es/(N)o] [N]:' in seen
    # explicit prompt: still overrides — never decorated with the label.
    assert 'Use Other [(Y)es/(N)o] [N]:' in seen
    # and the broken literal must NOT appear.
    assert 'None [(Y)es/(N)o] [N]:' not in seen


def test_generate_boolean_case_is_string_only(tmp):
    # test32: a type: boolean variable that ALSO declares case: → ValueError
    # (D-17: case:/validate: are string-only semantics; declaring either on
    # a boolean is a fail-fast schema misconfig).
    argv = ['generate', 'test32', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        with raises(ValueError, match="case.*string-only"):
            app.run()


def test_generate_boolean_silent(tmp):
    # test33: type: boolean with `prompt: false` (silent) emits bool(default)
    # at data[name] — a real Python bool, NOT str(default). The fixture uses
    # `default: false`, so a correctly-typed False renders the else branch
    # (flag-off). A regressed impl emitting the string 'False' would be
    # truthy → render flag-on → fail here, guarding the typed-output contract.
    argv = ['generate', 'test33', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        app.run()
        with open(os.path.join(tmp.dir, 'take-me')) as f:
            assert 'flag-off' in f.read()


def test_generate_invalid_type(tmp):
    # test34: a variable declaring an unknown `type:` → ValueError (T-05.1-01
    # input-validation mitigation; fail-fast, survives `python -O`).
    argv = ['generate', 'test34', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        with raises(ValueError, match="invalid type 'bogus'"):
            app.run()


def test_generate_features_transitive_requires(tmp):
    # test14: feature1=false gates feature2 (default false), which gates
    # feature3 (default false). Each gated-out variable resolves to its
    # own falsy default (Q1), so the cascade propagates: a downstream
    # `requires` against a gated-out var also fails. The resolved bool
    # values render into take-me; all three end up False.
    argv = ['generate', 'test14', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        app.run()

        assert exists_join(tmp.dir, 'take-me')
        with open(os.path.join(tmp.dir, 'take-me')) as f:
            res = f.read()
            # transitive cascade: all three gated-out to their False default
            assert 'feature1=False' in res
            assert 'feature2=False' in res
            assert 'feature3=False' in res

        # feature1 false: its when:false rule fires, feature1-only ignored
        assert not exists_join(tmp.dir, 'feature1-only')

        # feature2/feature3 gated out: their extend rules do NOT fire (Q1),
        # so their -only files stay
        assert exists_join(tmp.dir, 'feature2-only')
        assert exists_join(tmp.dir, 'feature3-only')


def test_generate_features_requires_out_of_order(tmp):
    # test15: feature_b (requires feature_a) is declared BEFORE feature_a.
    # Both default to true. The lazy recursive resolver resolves
    # feature_a on demand when feature_b's requires gate is checked, so
    # resolution is order-independent and both stay enabled regardless of
    # the YAML declaration order.
    argv = ['generate', 'test15', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        app.run()

        assert exists_join(tmp.dir, 'take-me')

        # both features stay enabled despite the out-of-order declaration
        assert exists_join(tmp.dir, 'feature_a-only')
        assert exists_join(tmp.dir, 'feature_b-only')


def test_generate_features_null_block(tmp):
    # test12: a type: boolean variable with an extend rule whose
    # variables/exclude/ignore sub-keys are all null → coalesce to empty
    # lists via the `... or []` idiom (no crash).
    argv = ['generate', 'test12', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        app.run()

        assert exists_join(tmp.dir, 'take-me')
        with open(os.path.join(tmp.dir, 'take-me')) as f:
            res = f.read()
            assert 'myapp' in res


def test_generate_bad_template_module(tmp):
    class BadModuleApp(TestApp):
        class Meta:
            extensions = ['jinja2', 'yaml', 'generate', 'alarm']
            template_handler = 'jinja2'
            template_module = 'nonexistent.templates'
            handlers = [GenerateBase]

    argv = ['generate', 'test1', tmp.dir, '--defaults']
    with BadModuleApp(argv=argv, template_dir='tests/data/templates') as app:
        app.run()

        assert exists_join(tmp.dir, 'take-me')


def test_generate_template_module_transitive_import_error(tmp):
    # When the template module itself exists but raises ModuleNotFoundError
    # for some other (transitive) module during import, setup_template_items
    # must propagate the error rather than silently swallowing it as a
    # generic "template module not found" debug log.
    class TransitiveBadApp(TestApp):
        class Meta:
            extensions = ['jinja2', 'yaml', 'generate', 'alarm']
            template_handler = 'jinja2'
            template_module = 'tests.data.bad_template_module'
            handlers = [GenerateBase]

    argv = ['generate', 'test1', tmp.dir, '--defaults']
    with raises(ModuleNotFoundError, match='nonexistent_transitive_dep'):
        with TransitiveBadApp(argv=argv,
                              template_dir='tests/data/templates') as app:
            app.run()


# ─── #779: prompt_mode: select multi-valued feature prompts ─────────────


def test_generate_choice_defaults(tmp):
    # test16: type: choice with three options; --defaults dispatches to
    # the variable default ("N"). The migrated fixture carries an
    # `extend.when: "N"` rule whose ignore patterns (branch-1-only,
    # branch-2-only) must FIRE via scalar str()-coerced equality;
    # branch-N-file and take-me remain.
    argv = ['generate', 'test16', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        app.run()

        assert exists_join(tmp.dir, 'take-me')
        assert exists_join(tmp.dir, 'branch-N-file')
        assert not exists_join(tmp.dir, 'branch-1-only')
        assert not exists_join(tmp.dir, 'branch-2-only')


# test17 (select_collision) and test18 (invalid_prompt_mode) were
# REMOVED in Plan 03: they asserted on the `prompt_mode`/`enabled`/
# `disabled` schema that ceases to exist once the legacy `features:`
# bridge is deleted. The `type:` whitelist they would have repurposed to
# is already covered by test_generate_invalid_type (test34, `type:
# bogus` → ValueError).


def test_generate_choice_silent_variable_via_extend(tmp):
    # test19: type: choice with a SCALAR options list (["1", "2"]);
    # --defaults dispatches to the default ("1"). The migrated fixture's
    # `extend.when: "1"` rule fires via scalar str()-coerced equality and
    # contributes a silent variable `chosen_version: v1-silent`
    # (prompt: false). The silent variable's default lands verbatim.
    argv = ['generate', 'test19', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        app.run()

        assert exists_join(tmp.dir, 'take-me')
        with open(os.path.join(tmp.dir, 'take-me')) as f:
            assert 'v1-silent' in f.read()


def test_generate_choice_default_not_in_values(tmp):
    # test20: choice default "X" but options only contains "Y" →
    # ValueError at config validation.
    argv = ['generate', 'test20', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        with raises(ValueError, match="is not in options values"):
            app.run()


def test_generate_choice_missing_value(tmp):
    # test21: a choice options branch object missing value: → ValueError.
    argv = ['generate', 'test21', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        with raises(ValueError, match="missing required key: value"):
            app.run()


def test_generate_features_top_level_silent_variable(tmp):
    # test22: top-level variable with `prompt: false` — silent
    # sentinel works outside select-mode features too. The default
    # lands verbatim in the rendered output.
    argv = ['generate', 'test22', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        app.run()

        assert exists_join(tmp.dir, 'take-me-silent')
        with open(os.path.join(tmp.dir, 'take-me-silent')) as f:
            res = f.read()
            assert 'myapp' in res
            assert 'top_level_silent_value' in res


def test_generate_features_legacy_null_variables(tmp):
    # test23: a type: boolean extend rule with
    # `variables: null, exclude: null, ignore: null` must coalesce
    # safely via the `rule.get(...) or []` idiom (no crash).
    argv = ['generate', 'test23', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        app.run()

        assert exists_join(tmp.dir, 'take-me')


def test_generate_features_select_null_variables(tmp):
    # test24: a type: choice extend rule with
    # `variables: null, exclude: null, ignore: null` must coalesce
    # safely via the same `rule.get(...) or []` idiom.
    argv = ['generate', 'test24', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        app.run()

        assert exists_join(tmp.dir, 'take-me')


def test_generate_features_select_requires_cascade(tmp):
    # test25: a type: choice variable has `requires: [bool_prereq]`
    # where bool_prereq defaults to false. The choice is GATED OUT: set
    # to its default and its extend rules do NOT fire (Q1), so the
    # options-branch ignore patterns never apply — `should-not-appear-1`
    # remains in the rendered tree.
    argv = ['generate', 'test25', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        app.run()

        assert exists_join(tmp.dir, 'take-me')
        assert exists_join(tmp.dir, 'should-not-appear-1')


def test_generate_choice_empty_options(tmp):
    # test26: type: choice with `options: []` → ValueError.
    argv = ['generate', 'test26', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        with raises(ValueError, match="no 'options'"):
            app.run()


def test_generate_features_silent_variable_no_default(tmp):
    # test27: top-level `prompt: false` variable with no `default:` →
    # AssertionError from the silent-variable short-circuit.
    argv = ['generate', 'test27', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        with raises(AssertionError,
                    match="prompt: false but no default"):
            app.run()


def test_generate_choice_missing_default(tmp):
    # test28: type: choice with no `default:` → ValueError. Without
    # `default`, --defaults dispatch would silently no-op (str(None)
    # matches no option); fail-fast at validation per CONTEXT.md
    # Decision F.
    argv = ['generate', 'test28', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        with raises(ValueError, match="has no 'default'"):
            app.run()


def test_generate_features_silent_variable_non_str_default(tmp):
    # test29: silent variable with a YAML-decoded non-string default
    # (`default: false` → Python bool) + `case: upper`. The silent
    # short-circuit must coerce to str BEFORE the case operation runs;
    # otherwise `False.upper()` raises AttributeError.
    argv = ['generate', 'test29', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        app.run()

        assert exists_join(tmp.dir, 'take-me')
        with open(os.path.join(tmp.dir, 'take-me')) as f:
            # `case: upper` applied to str(False) → "FALSE".
            assert 'silent_flag=FALSE' in f.read()


def test_generate_choice_duplicate_labels(tmp):
    # test30: two choice options with the same effective display label
    # ("Same Label") → ValueError. The numbered list would be ambiguous
    # so we reject at config-validation time.
    argv = ['generate', 'test30', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        with raises(ValueError, match="duplicate option labels"):
            app.run()


# ─── #782 Plan 02: type: choice picker + object-form boolean prompt ──────


def test_generate_choice_picker_maps_label_to_value(tmp):
    # test16 (interactive): patch shell.Prompt.prompt to return the
    # numbered-picker label for the "2" option ("Branch Two"). The
    # picker maps the chosen label → option value "2", and the
    # extend.when: "2" rule fires (ignores branch-N-file + branch-1-only;
    # branch-2-only survives).
    with patch.object(shell.Prompt, 'prompt', return_value='Branch Two'):
        argv = ['generate', 'test16', tmp.dir]
        with GenerateApp(argv=argv) as app:
            app.run()

            assert exists_join(tmp.dir, 'take-me')
            assert exists_join(tmp.dir, 'branch-2-only')
            assert not exists_join(tmp.dir, 'branch-N-file')
            assert not exists_join(tmp.dir, 'branch-1-only')


def test_generate_boolean_object_prompt_accept(tmp):
    # test35: object-form bool prompt {text, accept, reject}. A member
    # of accept (case-insensitive) → data[name] True → enabled branch.
    with patch.object(shell.Prompt, 'prompt', return_value='YAY'):
        argv = ['generate', 'test35', tmp.dir]
        with GenerateApp(argv=argv) as app:
            app.run()
            with open(os.path.join(tmp.dir, 'take-me')) as f:
                assert 'enabled' in f.read()


def test_generate_boolean_object_prompt_reject(tmp):
    # test35: a member of reject → data[name] False → disabled branch.
    with patch.object(shell.Prompt, 'prompt', return_value='No'):
        argv = ['generate', 'test35', tmp.dir]
        with GenerateApp(argv=argv) as app:
            app.run()
            with open(os.path.join(tmp.dir, 'take-me')) as f:
                assert 'disabled' in f.read()


def test_generate_boolean_object_prompt_empty_uses_default(tmp):
    # test35: empty input falls through to the var's bool default
    # (false) → disabled branch.
    with patch.object(shell.Prompt, 'prompt', return_value=''):
        argv = ['generate', 'test35', tmp.dir]
        with GenerateApp(argv=argv) as app:
            app.run()
            with open(os.path.join(tmp.dir, 'take-me')) as f:
                assert 'disabled' in f.read()


def test_generate_boolean_object_prompt_defaults(tmp):
    # test35 with --defaults: the object-form bool short-circuits to
    # bool(default) (false) without prompting → disabled branch.
    argv = ['generate', 'test35', tmp.dir, '--defaults']
    with GenerateApp(argv=argv) as app:
        app.run()
        with open(os.path.join(tmp.dir, 'take-me')) as f:
            assert 'disabled' in f.read()


def test_generate_boolean_object_prompt_junk_aborts(tmp):
    # test35: junk input matching NEITHER accept nor reject → assert +
    # abort with an "Invalid Response"-style message (D-14, mirrors
    # validate:). No silent coercion to False.
    with patch.object(shell.Prompt, 'prompt', return_value='maybe'):
        argv = ['generate', 'test35', tmp.dir]
        with GenerateApp(argv=argv) as app:
            with raises(AssertionError, match="Invalid Response.*"):
                app.run()


def test_generate_boolean_object_prompt_yaml_bool_coercion_guard(tmp):
    # test36: an accept:/reject: member that loaded as a Python bool
    # (YAML 1.1 coercion of bare `yes`) → ValueError at config load,
    # instructing the author to quote the bool-like token.
    argv = ['generate', 'test36', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        with raises(ValueError, match="quote"):
            app.run()


def test_generate_choice_case_is_string_only(tmp):
    # test37: a type: choice variable that ALSO declares case: →
    # ValueError (D-17: case:/validate: are string-only; declaring
    # either on a choice is a fail-fast schema misconfig).
    argv = ['generate', 'test37', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        with raises(ValueError, match="case.*string-only"):
            app.run()


# ─── #782 Plan 03: extend.when list/regex, nesting, requires: ────────────


def test_generate_extend_when_list_membership(tmp):
    # test38: choice value "flask" (default). The `when: [flask, fastapi]`
    # rule fires via in-list membership (ignores not-web); the
    # `when: [fastapi]` rule does NOT fire ("flask" not a member) so
    # fastapi-only is kept. Rules compose independently.
    argv = ['generate', 'test38', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        app.run()

        assert exists_join(tmp.dir, 'take-me')
        # when: [flask, fastapi] matched → not-web ignored
        assert not exists_join(tmp.dir, 'not-web')
        # when: [fastapi] did NOT match → fastapi-only kept
        assert exists_join(tmp.dir, 'fastapi-only')
        # boolean list-form: True is a member of [true] → fires
        assert not exists_join(tmp.dir, 'bool-list-ignored')


def test_generate_requires_dict_equality(tmp):
    # test41: dict-form `requires: {name: value}` equality. dep_ok
    # requires mode == "advanced" (satisfied → its extend fires,
    # dep-ok-ignored removed); dep_no requires mode == "basic" (NOT
    # satisfied → gated out, renders its default "no", extend does NOT
    # fire so dep-no-kept survives).
    argv = ['generate', 'test41', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        app.run()

        with open(os.path.join(tmp.dir, 'take-me')) as f:
            res = f.read()
            assert 'mode=advanced' in res
            assert 'dep_ok=ok' in res
            # gated-out dep_no still renders its default (Q1)
            assert 'dep_no=no' in res

        # dep_ok requires satisfied → its extend fired
        assert not exists_join(tmp.dir, 'dep-ok-ignored')
        # dep_no gated out → its extend did NOT fire
        assert exists_join(tmp.dir, 'dep-no-kept')


def test_generate_extend_when_string_regex(tmp):
    # test39: a type: string variable resolving to "v2.1". The
    # `when: "^v2"` rule fires via re.match (string-type regex; ignores
    # not-v2); the `when: "^v3"` rule does NOT match so v3-only is kept.
    argv = ['generate', 'test39', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        app.run()

        assert exists_join(tmp.dir, 'take-me')
        # ^v2 matched "v2.1" → not-v2 ignored
        assert not exists_join(tmp.dir, 'not-v2')
        # ^v3 did NOT match → v3-only kept
        assert exists_join(tmp.dir, 'v3-only')


def test_generate_requires_gated_out_renders_default(tmp):
    # test40 (Q1): prereq=false gates `dependent`. The gated-out var is
    # set to its `default` at data[name] (renders "fallback", never
    # KeyErrors) AND its extend rule does NOT fire — even though
    # `when: "fallback"` would match the default value — so
    # should-be-kept survives.
    argv = ['generate', 'test40', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        app.run()

        with open(os.path.join(tmp.dir, 'take-me')) as f:
            # gated-out dependent renders as its default (Q1)
            assert 'fallback' in f.read()

        # the gated-out var's extend rule did NOT fire (Q1)
        assert exists_join(tmp.dir, 'should-be-kept')
