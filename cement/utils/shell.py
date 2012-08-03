"""Common Shell Utilities."""

from subprocess import Popen, PIPE
            
def exec_cmd(cmd_args, shell=False):
    """
    Execute a shell call using Subprocess.
    
    :param cmd_args: List of command line arguments.
    :type cmd_args: list
    :param shell: See `Subprocess <http://docs.python.org/library/subprocess.html>`_
    :type shell: boolean
    :returns: The (stdout, stderror, return_code) of the command
    :rtype: tuple
    
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
    :param shell: See `Subprocess <http://docs.python.org/library/subprocess.html>`_
    :type shell: boolean
    :returns: The integer return code of the command.
    :rtype: int
    
    """
    proc = Popen(cmd_args, shell=shell)
    proc.wait()
    return proc.returncode