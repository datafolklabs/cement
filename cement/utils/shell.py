"""Common Shell Utilities."""

from subprocess import Popen, PIPE
from multiprocessing import Process
from threading import Thread


def exec_cmd(cmd_args, shell=False):
    """
    Execute a shell call using Subprocess.

    :param cmd_args: List of command line arguments.
    :type cmd_args: list
    :param shell: See `Subprocess
        <http://docs.python.org/library/subprocess.html>`_
    :type shell: boolean
    :returns: The (stdout, stderror, return_code) of the command
    :rtype: tuple

    Usage:

    .. code-block:: python

        from cement.utils import shell

        stdout, stderr, exitcode = shell.exec_cmd(['echo', 'helloworld'])

    """
    proc = Popen(cmd_args, stdout=PIPE, stderr=PIPE, shell=shell)
    (stdout, stderr) = proc.communicate()
    proc.wait()
    return (stdout, stderr, proc.returncode)


def exec_cmd2(cmd_args, shell=False):
    """
    Similar to exec_cmd, however does not capture stdout, stderr (therefore
    allowing it to print to console).

    :param cmd_args: List of command line arguments.
    :type cmd_args: list
    :param shell: See `Subprocess
        <http://docs.python.org/library/subprocess.html>`_
    :type shell: boolean
    :returns: The integer return code of the command.
    :rtype: int

    Usage:

    .. code-block:: python

        from cement.utils import shell

        exitcode = shell.exec_cmd2(['echo', 'helloworld'])

    """
    proc = Popen(cmd_args, shell=shell)
    proc.wait()
    return proc.returncode


def spawn_process(target, start=True, join=False, *args, **kwargs):
    """
    A quick wrapper around multiprocessing.Process().  By default the start()
    function will be called before the spawned process object is returned.

    :param target: The target function to execute in the sub-process.
    :param start: Call start() on the process before returning the process
        object.
    :param join: Call join() on the process before returning the process
        object.  Only called if start=True.
    :param args: Additional arguments are passed to Process().
    :param kwargs: Additional keyword arguments are passed to Process().
    :returns: The process object returned by Process().

    Usage:

    .. code-block:: python

        from cement.utils import shell

        def add(a, b):
            print(a + b)

        p = shell.spawn_process(add, args=(12, 27))
        p.join()

    """
    proc = Process(target=target, *args, **kwargs)

    if start and not join:
        proc.start()
    elif start and join:
        proc.start()
        proc.join()
    return proc


def spawn_thread(target, start=True, join=False, *args, **kwargs):
    """
    A quick wrapper around threading.Thread().  By default the start()
    function will be called before the spawned thread object is returned

    :param target: The target function to execute in the thread.
    :param start: Call start() on the thread before returning the thread
        object.
    :param join: Call join() on the thread before returning the thread
        object.  Only called if start=True.
    :param args: Additional arguments are passed to Thread().
    :param kwargs: Additional keyword arguments are passed to Thread().
    :returns: The thread object returned by Thread().

    Usage:

    .. code-block:: python

        from cement.utils import shell

        def add(a, b):
            print(a + b)

        t = shell.spawn_thread(add, args=(12, 27))
        t.join()

    """
    thr = Thread(target=target, *args, **kwargs)

    if start and not join:
        thr.start()
    elif start and join:
        thr.start()
        thr.join()
    return thr
