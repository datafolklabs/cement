"""Common Shell Utilities."""

from subprocess import Popen, PIPE
            
def exec_cmd(cmd_args, shell=False):
    """
    Execute a shell call using Subprocess.
    
    Required Arguments:
    
        cmd_args
            List of command line arguments.
            
        shell
            Boolean option.  See `Subprocess <http://docs.python.org/library/subprocess.html>`_
            Default: False
            
    Return: tuple (stdout, stderr, return_code)
    
    """
    proc = Popen(cmd_args, stdout=PIPE, stderr=PIPE, shell=shell)
    (stdout, stderr) = proc.communicate()
    proc.wait()
    return (stdout, stderr, proc.returncode)
    
def exec_cmd2(cmd_args, shell=False):
    """
    Similar to exec_cmd, however does not capture stdout, stderr (therefore
    allowing it to print to console).
    
    Required Arguments:
    
        cmd_args
            List of command line arguments.
            
        shell
            Boolean option.  See `Subprocess <http://docs.python.org/library/subprocess.html>`_
            Default: False
            
    Return: int (return_code)
    
    """
    proc = Popen(cmd_args, shell=shell)
    proc.wait()
    return proc.returncode