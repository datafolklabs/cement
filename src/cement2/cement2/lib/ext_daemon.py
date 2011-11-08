"""
Daemon Framework Extension Library.

This module is used to fork the current process into a daemon.

Almost none of this is necessary (or advisable) if your daemon is being started
by inetd. In that case, stdin, stdout and stderr are all set up for you to
refer to the network connection, and the fork()s and session manipulation
should not be done (to avoid confusing inetd). Only the chdir() and umask()
steps remain useful.

References:

    UNIX Programming FAQ
        1.7 How do I get my program to act like a daemon?
        http://www.unixguide.net/unix/programming/1.7.shtml
        http://www.faqs.org/faqs/unix-faq/programmer/faq/

    Advanced Programming in the Unix Environment
        W. Richard Stevens, 1992, Addison-Wesley, ISBN 0-201-56317-7.

"""

import sys
import os
import pwd
import grp
from cement2.core import backend, exc

Log = backend.minimal_logger(__name__)

class Context(object):
    def __init__(self, **kw):
        self.stdin = kw.get('stdin', '/dev/null')
        self.stdout = kw.get('stdout', '/dev/null')
        self.stderr = kw.get('stderr', '/dev/null')
        self.dir = kw.get('directory', os.curdir)
        self.pid_file = kw.get('pid_file', None)
        self.user_name = kw.get('user_name', 
                                os.environ['USER'])
            
        # clean up
        self.dir = os.path.abspath(os.path.expanduser(self.dir))
        if self.pid_file:
            self.pid_file = os.path.abspath(os.path.expanduser(self.pid_file))
                                
        try:
            self.user = pwd.getpwnam(self.user_name)
        except KeyError, e:
            raise exc.CementRuntimeError("Daemon user '%s' doesn't exist." % \
                                         self.user_name)
                                         
        try:
            self.group_name = kw.get('group_name', 
                                     grp.getgrgid(self.user.pw_gid))
            self.group = grp.getgrnam(self.group_name)
        except KeyError, e:
            raise exc.CementRuntimeError("Daemon group '%s' doesn't exist." % \
                                         self.group_name)
        
    def write_pid_file(self):
        # setup pid
        if self.pid_file:            
            f = open(self.pid_file, 'w')
            f.write(str(os.getpid()))
            f.close()
            os.chown(os.path.dirname(self.pid_file), 
                     self.user.pw_uid, self.group.gr_gid)
                                 
    def switch(self):
        # set the running uid/gid
        Log.debug('setting process uid(%s) and gid(%s)' % \
                 (self.user.pw_uid, self.group.gr_gid))
        os.setgid(self.group.gr_gid)
        os.setuid(self.user.pw_uid)
        os.environ['HOME'] = self.user.pw_dir
        if os.path.exists(self.pid_file):
            raise exc.CementRuntimeError, \
                "Process already running (%s)" % self.pid_file
        else:
            self.write_pid_file()
          
        # change directory
        os.chdir(os.path.abspath(self.dir))
         
    def daemonize(self):
        """
        This forks the current process into a daemon.
        
        References:

        UNIX Programming FAQ
            1.7 How do I get my program to act like a daemon?
            http://www.unixguide.net/unix/programming/1.7.shtml
            http://www.faqs.org/faqs/unix-faq/programmer/faq/

        Advanced Programming in the Unix Environment
            W. Richard Stevens, 1992, Addison-Wesley, ISBN 0-201-56317-7.

        """
    
        # Do first fork.
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)   # Exit first parent.
        except OSError, e:
            sys.stderr.write("Fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))
            sys.exit(1)

        # Decouple from parent environment.
        os.chdir('/')
        os.umask(0)
        os.setsid()

        # Do second fork.
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)   # Exit second parent.
        except OSError, e:
            sys.stderr.write("Fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))
            sys.exit(1)

        # Redirect standard file descriptors.
        stdin = open(self.stdin, 'r')
        stdout = open(self.stdout, 'a+')
        stderr = open(self.stderr, 'a+', 0)
        os.dup2(stdin.fileno(), sys.stdin.fileno())
        os.dup2(stdout.fileno(), sys.stdout.fileno())
        os.dup2(stderr.fileno(), sys.stderr.fileno())       
                 
        # Update our pid file
        self.write_pid_file()