"""Tests for cement.utils.shell"""

import sys
import time
import mock
from cement.utils import shell, test
from cement.core.exc import FrameworkError

if sys.version_info[0] < 3:
    INPUT = '__builtin__.raw_input'
else:
    INPUT = 'builtins.input'


def add(a, b):
    return a + b


class ShellUtilsTestCase(test.CementCoreTestCase):

    def test_exec_cmd(self):
        out, err, ret = shell.exec_cmd(['echo', 'KAPLA!'])
        self.eq(ret, 0)
        self.eq(out, b'KAPLA!\n')

    def test_exec_cmd_shell_true(self):
        out, err, ret = shell.exec_cmd(['echo KAPLA!'], shell=True)
        self.eq(ret, 0)
        self.eq(out, b'KAPLA!\n')

    def test_exec_cmd2(self):
        ret = shell.exec_cmd2(['echo'])
        self.eq(ret, 0)

    def test_exec_cmd2_shell_true(self):
        ret = shell.exec_cmd2(['echo johnny'], shell=True)
        self.eq(ret, 0)

    def test_exec_cmd_bad_command(self):
        out, err, ret = shell.exec_cmd(['false'])
        self.eq(ret, 1)

    def test_exec_cmd2_bad_command(self):
        ret = shell.exec_cmd2(['false'])
        self.eq(ret, 1)

    def test_spawn_process(self):
        p = shell.spawn_process(add, args=(23, 2))
        p.join()
        self.eq(p.exitcode, 0)

        p = shell.spawn_process(add, join=True, args=(23, 2))
        self.eq(p.exitcode, 0)

    def test_spawn_thread(self):
        t = shell.spawn_thread(time.sleep, args=(2,))

        # before joining it is alive
        res = t.is_alive()
        self.eq(res, True)

        t.join()

        # after joining it is not alive
        res = t.is_alive()
        self.eq(res, False)

        t = shell.spawn_thread(time.sleep, join=True, args=(2,))
        res = t.is_alive()
        self.eq(res, False)

    def test_prompt_simple(self):
        with mock.patch(INPUT, return_value='Test Input'):
            p = shell.Prompt("Test Prompt")
            self.eq(p.input, 'Test Input')

    def test_prompt_clear(self):
        # test with a non-clear command:
        with mock.patch(INPUT, return_value='Test Input'):
            p = shell.Prompt("Test Prompt",
                             clear=True,
                             clear_command='true',
                             )
            self.eq(p.input, 'Test Input')

    def test_prompt_options(self):
        # test options (non-numbered.. user inputs actual option)
        with mock.patch(INPUT, return_value='y'):
            p = shell.Prompt("Test Prompt", options=['y', 'n'])
            self.eq(p.input, 'y')

        # test default value
        with mock.patch(INPUT, return_value=''):
            p = shell.Prompt("Test Prompt", options=['y', 'n'], default='n')
            self.eq(p.input, 'n')

    def test_prompt_numbered_options(self):
        # test numbered selection (user inputs number)
        with mock.patch(INPUT, return_value='3'):
            p = shell.Prompt("Test Prompt",
                             options=['yes', 'no', 'maybe'],
                             numbered=True,
                             )
            self.eq(p.input, 'maybe')

        # test default value
        with mock.patch(INPUT, return_value=''):
            p = shell.Prompt(
                "Test Prompt",
                options=['yes', 'no', 'maybe'],
                numbered=True,
                default='2',
            )
            self.eq(p.input, 'no')

    def test_prompt_input_is_none(self):
        # test that self.input is none if no default, and no input
        with mock.patch(INPUT, return_value=''):
            p = shell.Prompt('Test Prompt',
                             max_attempts=3,
                             max_attempts_exception=False,
                             )
            self.eq(p.input, None)

    @test.raises(FrameworkError)
    def test_prompt_max_attempts(self):
        # test that self.input is none if no default, and no input
        with mock.patch(INPUT, return_value=''):
            try:
                p = shell.Prompt('Test Prompt',
                                 max_attempts=3,
                                 max_attempts_exception=True,
                                 )
            except FrameworkError as e:
                self.eq(e.msg,
                        "Maximum attempts exceeded getting valid user input",
                        )
                raise

    def test_prompt_index_and_value_errors(self):
        with mock.patch(INPUT, return_value='5'):
            p = shell.Prompt(
                "Test Prompt",
                options=['yes', 'no', 'maybe'],
                numbered=True,
                max_attempts=3,
                max_attempts_exception=False,
            )
            self.eq(p.input, None)

    def test_prompt_case_insensitive(self):
        with mock.patch(INPUT, return_value='NO'):
            p = shell.Prompt(
                "Test Prompt",
                options=['yes', 'no', 'maybe'],
                case_insensitive=True,
            )
            self.eq(p.input, 'NO')

        with mock.patch(INPUT, return_value='NOT VALID'):
            p = shell.Prompt(
                "Test Prompt",
                options=['yes', 'no', 'maybe'],
                case_insensitive=True,
                max_attempts=3,
                max_attempts_exception=False,
            )
            self.eq(p.input, None)

    def test_prompt_case_sensitive(self):
        with mock.patch(INPUT, return_value='NO'):
            p = shell.Prompt(
                "Test Prompt",
                options=['yes', 'no', 'maybe'],
                case_insensitive=False,
                max_attempts=3,
                max_attempts_exception=False,
            )
            self.eq(p.input, None)
