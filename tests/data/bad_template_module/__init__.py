# Fixture: a real Python package whose import raises ModuleNotFoundError
# for a *different* module name than the package itself. Used by
# tests/ext/test_ext_generate.py to verify that setup_template_items
# propagates transitive ModuleNotFoundError raised inside the user's
# template module instead of silently swallowing it as "module not found".
import nonexistent_transitive_dep  # noqa: F401
