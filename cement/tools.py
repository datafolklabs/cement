"""Common tools."""

import os
from subprocess import Popen, PIPE

def abspath(path):
    return os.path.abspath(os.path.expanduser(path))
    
def exec_cmd(cmd_args):
    proc = Popen(cmd_args, stdout=PIPE, stderr=PIPE)
    (stdout, stderr) = proc.communicate()
    proc.wait()
    return (stdout, stderr, proc.returncode)
    
def exec_cmd2(cmd_args):
    proc = Popen(cmd_args)
    proc.wait()
    return proc.returncode
