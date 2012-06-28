"""
Daemon Framework Extension Library.
        
"""

import os
import io
import sys
import pwd
import grp
from ..core import backend, exc

Log = backend.minimal_logger(__name__)

class Environment(object):
    """
    This class provides a mechanism for altering the running processes
    environment.
    
    Optional Arguments:
    
        stdin
            A file to read STDIN from.  Default: /dev/null
            
        stdout
            A file to write STDOUT to.  Default: /dev/null
        
        stderr
            A file to write STDERR to.  Default: /dev/null
            
        dir
            The directory to run the process in.
        
        pid_file
            The filesystem path to where the PID (Process ID) should be 
            written to.  Default: None
        
        user_name
            The user name to run the process as.  Default: os.environ['USER']
        
        group_name
            The group name to run the process as.  Default: The primary group
            of os.environ['USER'].
        
        umask
            The umask to pass to os.umask().  Default: 0
        
    """
    def __init__(self, **kw):
        self.stdin = kw.get('stdin', '/dev/null')
        self.stdout = kw.get('stdout', '/dev/null')
        self.stderr = kw.get('stderr', '/dev/null')
        self.dir = kw.get('dir', os.curdir)
        self.pid_file = kw.get('pid_file', None)
        self.umask = kw.get('umask', 0)
        self.user_name = kw.get('user_name', 
                                os.environ['USER'])
            
        # clean up
        self.dir = os.path.abspath(os.path.expanduser(self.dir))
        if self.pid_file:
            self.pid_file = os.path.abspath(os.path.expanduser(self.pid_file))
                                
        try:
            self.user = pwd.getpwnam(self.user_name)
        except KeyError as e:
            raise exc.CementRuntimeError("Daemon user '%s' doesn't exist." % \
                                         self.user_name)
                                         
        try:
            self.group_name = kw.get('group_name', 
                                     grp.getgrgid(self.user.pw_gid).gr_name)
            self.group = grp.getgrnam(self.group_name)
        except KeyError as e:
            raise exc.CementRuntimeError("Daemon group '%s' doesn't exist." % \
                                         self.group_name)
        
    def _write_pid_file(self):
        """
        Writes os.getpid() out to self.pid_file.
        
        """
        pid = str(os.getpid())
        Log.debug('writing pid (%s) out to %s' % (pid, self.pid_file))
        
        # setup pid
        if self.pid_file:            
            f = open(self.pid_file, 'w')
            f.write(pid)
            f.close()
            try:
                os.chown(os.path.dirname(self.pid_file), 
                         self.user.pw_uid, self.group.gr_gid)
            except OSError as e:
                Log.debug("unable to chown %s:%s %s" % \
                         (self.user.pw_uid, self.group.gr_gid, self.pid_file))
                         
    def switch(self):
        """
        Switch the current process's user/group to self.user_name, and 
        self.group_name.  Change directory to self.dir, and write the 
        current pid out to self.pid_file.
        
        """
        # set the running uid/gid
        Log.debug('setting process uid(%s) and gid(%s)' % \
                 (self.user.pw_uid, self.group.gr_gid))
        os.setgid(self.group.gr_gid)
        os.setuid(self.user.pw_uid)
        os.environ['HOME'] = self.user.pw_dir
        os.chdir(self.dir)
        if self.pid_file and os.path.exists(self.pid_file):
            raise exc.CementRuntimeError("Process already running (%s)" % \
                                         self.pid_file)
        else:
            self._write_pid_file()
         
    def daemonize(self):
        """
        Fork the current process into a daemon.
        
        References:

        UNIX Programming FAQ
            1.7 How do I get my program to act like a daemon?
            http://www.unixguide.net/unix/programming/1.7.shtml
            http://www.faqs.org/faqs/unix-faq/programmer/faq/

        Advanced Programming in the Unix Environment
            W. Richard Stevens, 1992, Addison-Wesley, ISBN 0-201-56317-7.

        """
        Log.debug('attempting to daemonize the current process')
        # Do first fork.
        try:
            pid = os.fork()
            if pid > 0:
                Log.debug('successfully detached from first parent')
                os._exit(os.EX_OK)
        except OSError as e:
            sys.stderr.write("Fork #1 failed: (%d) %s\n" % \
                            (e.errno, e.strerror))
            sys.exit(1)

        # Decouple from parent environment.
        os.chdir(self.dir)
        os.umask(int(self.umask))
        os.setsid()

        # Do second fork.
        try:
            pid = os.fork()
            if pid > 0:
                Log.debug('successfully detached from second parent')
                os._exit(os.EX_OK)
        except OSError as e:
            sys.stderr.write("Fork #2 failed: (%d) %s\n" % \
                            (e.errno, e.strerror))
            sys.exit(1)

        # Redirect standard file descriptors.
        stdin = open(self.stdin, 'r')
        stdout = open(self.stdout, 'a+')
        stderr = open(self.stderr, 'a+')
        
        if hasattr(sys.stdin, 'fileno'):
            try:
                os.dup2(stdin.fileno(), sys.stdin.fileno())
            except io.UnsupportedOperation as e:
                # FIXME: ?
                pass
        if hasattr(sys.stdout, 'fileno'):
            try:
                os.dup2(stdout.fileno(), sys.stdout.fileno())
            except io.UnsupportedOperation as e:
                # FIXME: ?
                pass
        if hasattr(sys.stderr, 'fileno'):    
            try:
                os.dup2(stderr.fileno(), sys.stderr.fileno())       
            except io.UnsupportedOperation as e:
                # FIXME: ?
                pass
                 
        # Update our pid file
        self._write_pid_file()