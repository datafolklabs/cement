
import os
import subprocess

from cement.cli.main import CementTestApp as App
from cement.cli.main import main
from cement.utils.test import raises


def test_main(tmp):
    with raises(SystemExit):
        main()


def test_app():
    argv = []

    with App(argv=argv) as app:
        no_base_controller_retval = app.run()
        assert no_base_controller_retval is None


def test_generate(tmp):
    argv = ['generate', 'project', tmp.dir, '--defaults']

    with App(argv=argv) as app:
        app.run()

        assert os.path.exists(os.path.join(tmp.dir, 'pyproject.toml'))


def test_generate_todo_ruff_clean(tmp):
    # Regression guard: generate a todo-tutorial and re-run ruff against the
    # RENDERED output. CI's cli-smoke-test todo block is build/install-only
    # (D-07), so this is the only gate that catches a future template
    # import-order (I001) regression in the shipped todo/ package. Running
    # ``ruff check .`` from the generated dir resolves that project's
    # ``[tool.ruff]`` tests-excluded scope, exercising the exact shipped gate.
    argv = ['generate', 'todo-tutorial', tmp.dir, '--defaults']

    with App(argv=argv) as app:
        app.run()

    result = subprocess.run(
        ['ruff', 'check', '.'],
        cwd=tmp.dir,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, (
        f'ruff check failed on generated todo-tutorial:\n'
        f'stdout:\n{result.stdout}\nstderr:\n{result.stderr}'
    )
