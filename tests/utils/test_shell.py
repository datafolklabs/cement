
import sys
import time
import mock
from pytest import raises

from cement.utils import shell
from cement.core.exc import FrameworkError

INPUT = 'builtins.input'


def add(a, b):
    return a + b


def test_exec_cmd():
    out, err, ret = shell.exec_cmd(['echo', 'KAPLA!'])
    assert ret == 0
    assert out == b'KAPLA!\n'


def test_exec_cmd_shell_true():
    out, err, ret = shell.exec_cmd(['echo KAPLA!'], shell=True)
    assert ret == 0
    assert out == b'KAPLA!\n'


def test_exec_cmd2():
    ret = shell.exec_cmd2(['echo'])
    assert ret == 0


def test_exec_cmd2_shell_true():
    ret = shell.exec_cmd2(['echo johnny'], shell=True)
    assert ret == 0


def test_exec_cmd_bad_command():
    out, err, ret = shell.exec_cmd(['false'])
    assert ret == 1


def test_exec_cmd2_bad_command():
    ret = shell.exec_cmd2(['false'])
    assert ret == 1


def test_spawn_process():
    p = shell.spawn_process(add, args=(23, 2))
    p.join()
    assert p.exitcode == 0

    p = shell.spawn_process(add, join=True, args=(23, 2))
    assert p.exitcode == 0


def test_spawn_thread():
    t = shell.spawn_thread(time.sleep, args=(2,))

    # before joining it is alive
    res = t.is_alive()
    assert res is True

    t.join()

    # after joining it is not alive
    res = t.is_alive()
    assert res is False

    t = shell.spawn_thread(time.sleep, join=True, args=(2,))
    res = t.is_alive()
    assert res is False


def test_prompt_simple():
    with mock.patch(INPUT, return_value='Test Input'):
        p = shell.Prompt("Test Prompt")
        assert p.input == 'Test Input'


def test_prompt_clear():
    # test with a non-clear command:
    with mock.patch(INPUT, return_value='Test Input'):
        p = shell.Prompt("Test Prompt",
                         clear=True,
                         clear_command='true',
                         )
        assert p.input == 'Test Input'


def test_prompt_options():
    # test options (non-numbered.. user inputs actual option)
    with mock.patch(INPUT, return_value='y'):
        p = shell.Prompt("Test Prompt", options=['y', 'n'])
        assert p.input == 'y'

    # test default value
    with mock.patch(INPUT, return_value=''):
        p = shell.Prompt("Test Prompt", options=['y', 'n'], default='n')
        assert p.input == 'n'


def test_prompt_numbered_options():
    # test numbered selection (user inputs number)
    with mock.patch(INPUT, return_value='3'):
        p = shell.Prompt("Test Prompt",
                         options=['yes', 'no', 'maybe'],
                         numbered=True,
                         )
        assert p.input == 'maybe'

    # test default value
    with mock.patch(INPUT, return_value=''):
        p = shell.Prompt(
            "Test Prompt",
            options=['yes', 'no', 'maybe'],
            numbered=True,
            default='2',
        )
        assert p.input == 'no'


def test_prompt_input_is_none():
    # test that self.input is none if no default, and no input
    with mock.patch(INPUT, return_value=''):
        p = shell.Prompt('Test Prompt',
                         max_attempts=3,
                         max_attempts_exception=False,
                         )
        assert p.input is None


def test_prompt_max_attempts():
    # test that self.input is none if no default, and no input
    with mock.patch(INPUT, return_value=''):
        msg = "Maximum attempts exceeded getting valid user input"
        with raises(FrameworkError, match=msg):
            shell.Prompt('Test Prompt',
                         max_attempts=3,
                         max_attempts_exception=True,
                         )


def test_prompt_index_and_value_errors():
    with mock.patch(INPUT, return_value='5'):
        p = shell.Prompt(
            "Test Prompt",
            options=['yes', 'no', 'maybe'],
            numbered=True,
            max_attempts=3,
            max_attempts_exception=False,
        )
        assert p.input is None


def test_prompt_case_insensitive():
    with mock.patch(INPUT, return_value='NO'):
        p = shell.Prompt(
            "Test Prompt",
            options=['yes', 'no', 'maybe'],
            case_insensitive=True,
        )
        assert p.input == 'NO'

    with mock.patch(INPUT, return_value='NOT VALID'):
        p = shell.Prompt(
            "Test Prompt",
            options=['yes', 'no', 'maybe'],
            case_insensitive=True,
            max_attempts=3,
            max_attempts_exception=False,
        )
        assert p.input is None


def test_prompt_case_sensitive():
    with mock.patch(INPUT, return_value='NO'):
        p = shell.Prompt(
            "Test Prompt",
            options=['yes', 'no', 'maybe'],
            case_insensitive=False,
            max_attempts=3,
            max_attempts_exception=False,
        )
        assert p.input is None
