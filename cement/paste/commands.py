"""
Paste commands to a generate a new Cement projects and plugins.

Create a new project named helloworld with this command:

    $ paster cement-app helloworld
    
    
Create a new plugin for the helloworld project with this command:

    $ paster cement-plugin helloworld myplugin
    

Usage:

.. parsed-literal::

    paster cement-app [--version][-h|--help]
            [--dry-run][-t|--templates *TEMPLATES*]

.. container:: paster-usage

  --version
      show program's version number and exit
  -h, --help
      show this help message and exit
  --dry-run
      dry run (don't actually do anything)
  -t *TEMPLATES*, --templates=*TEMPLATES*
      user specific template
    
"""

# Taken mostly from tg.devtools... Thank you! 

import sys, os
import re
import pkg_resources
import optparse
from paste.script import command
from paste.script import create_distro

beginning_letter = re.compile(r"^[^a-z]*")
valid_only = re.compile(r"[^a-z0-9_]")

from cement.core.configuration import CEMENT_ABI

CEMENT_VERSION = pkg_resources.get_distribution('cement').version

(base, major) = CEMENT_VERSION.split('.')[:2]
CEMENT_NEXT_VERSION = float("%s.%s" % (base, major)) + 0.1

class CementAppCommand(command.Command):
    """Create a new CLI Application using the Cement Framework.

Example usage::

    $ paster cement-app yourproject
    """
    version = CEMENT_VERSION
    summary = __doc__.splitlines()[0]
    usage = '\n' + __doc__
    name = None
    group_name = "Cement"
    dry_run = False
    templates = "cementapp"
    
    parser = command.Command.standard_parser(quiet=True)
    parser = optparse.OptionParser(
        usage="%prog cement-app [options] [project name]",
        version="%prog " + version
        )
    parser.add_option("-t", "--templates",
        help="user specific templates",
        dest="templates", default=templates
        )
    parser.add_option("--dry-run",
        help="dry run (don't actually do anything)",
        action="store_true", dest="dry_run"
        )
    
    def command(self):
        """LayCement for the new project."""
        
        self.__dict__.update(self.options.__dict__)
        
        if self.args:
            self.name = self.args[0]

        while not self.name:
            self.name = raw_input("Enter project name: ")
            
        package = self.name.lower()
        package = beginning_letter.sub("", package)
        package = valid_only.sub("_", package)
        if package:
            self.package = package
        else:
            self.package = None
            while not self.package:
                self.package = raw_input(
                    "Enter package name [%s]: " % package).strip() or package
        
        self.name = pkg_resources.safe_name(self.name)
    
        env = pkg_resources.Environment()
        if self.name.lower() in env:
            print 'The name "%s" is already in use by' % self.name,
            for dist in env[self.name]:
                print dist
                return

        import imp
        try:
            if imp.find_module(self.package):
                print 'The package name "%s" is already in use' % self.package
                return
        except ImportError:
            pass

        if os.path.exists(self.name):
            print 'A directory called "%s" already exists. Exiting.' % self.name
            return
        
        command = create_distro.CreateDistroCommand("create")
        cmd_args = []
        for template in self.templates.split():
            cmd_args.append("--template=%s" % template)
        cmd_args.append(self.name)
        cmd_args.append("cement_abi=%s" % CEMENT_ABI)
        cmd_args.append("cement_version=%s" % CEMENT_VERSION)
        cmd_args.append("cement_next_version=%s" % CEMENT_NEXT_VERSION)
        command.run(cmd_args)
        
        if not self.dry_run:
            sys.argv = ["setup.py", "egg_info"]
            
            # dirty hack to allow "empty" dirs
            for base, path, files in os.walk("./"):
                for file in files:
                    if file == "empty":
                        os.remove(os.path.join(base, file))


class CementPluginCommand(command.Command):
    """Create a plugin for an application using the Cement Framework.

Example usage::

    $ paster cement-plugin yourproject yourplugin
    """
    version = CEMENT_VERSION
    summary = __doc__.splitlines()[0]
    usage = '\n' + __doc__
    name = None
    group_name = "Cement"
    dry_run = False
    templates = "cementplugin"
    project = None
    plugin = None
    
    parser = command.Command.standard_parser(quiet=True)
    parser = optparse.OptionParser(
        usage="%prog cement-plugin [options] [project name] [plugin_name]",
        version="%prog " + version
        )
    parser.add_option("-t", "--templates",
        help="user specific templates",
        dest="templates", default=templates
        )
    parser.add_option("--dry-run",
        help="dry run (don't actually do anything)",
        action="store_true", dest="dry_run"
        )
    
    def command(self):
        """LayCement for the new project plugin."""
        
        self.__dict__.update(self.options.__dict__)
        
        if self.args:
            try:
                self.project = self.args[0].lower()
                self.plugin = self.args[1].lower()
            except IndexError:
                pass
        
        while not self.project:
            self.project = raw_input("Enter project name: ").lower()
        while not self.plugin:
            self.plugin = raw_input("Enter plugin name: ").lower()
            
        package = "%s-plugins-%s" % (self.project, self.plugin)
        package = beginning_letter.sub("", package)
        package = valid_only.sub("_", package)
        if package:
            self.package = package
        else:
            self.package = None
            while not self.package:
                self.package = raw_input(
                    "Enter package name [%s]: " % package).strip() or package
        
        self.name = pkg_resources.safe_name(self.package)
    
        env = pkg_resources.Environment()
        if self.name.lower() in env:
            print 'The name "%s" is already in use by' % self.name,
            for dist in env[self.name]:
                print dist
                return

        import imp
        try:
            if imp.find_module(self.package):
                print 'The package name "%s" is already in use' % self.package
                return
        except ImportError:
            pass

        if os.path.exists(self.name):
            print 'A directory called "%s" already exists. Exiting.' % self.name
            return
        
        command = create_distro.CreateDistroCommand("create")
        cmd_args = []
        for template in self.templates.split():
            cmd_args.append("--template=%s" % template)
        cmd_args.append(self.name)
        cmd_args.append("project=%s" % self.project)
        cmd_args.append("plugin=%s" % self.plugin)
        cmd_args.append("cement_abi=%s" % CEMENT_ABI)
        cmd_args.append("cement_version=%s" % CEMENT_VERSION)
        cmd_args.append("cement__next_version=%s" % CEMENT_NEXT_VERSION)
        
        command.run(cmd_args)
        
        if not self.dry_run:
            sys.argv = ["setup.py", "egg_info"]
            
            # dirty hack to allow "empty" dirs
            for base, path, files in os.walk("./"):
                for file in files:
                    if file == "empty":
                        os.remove(os.path.join(base, file))      
                        

class CementHelperCommand(command.Command):
    """Create a helper for an application using the Cement Framework.

Example usage::

    $ paster cement-helper yourproject yourplugin
    """
    version = CEMENT_VERSION
    summary = __doc__.splitlines()[0]
    usage = '\n' + __doc__
    name = None
    group_name = "Cement"
    dry_run = False
    templates = "cementhelper"
    project = None
    plugin = None
    
    parser = command.Command.standard_parser(quiet=True)
    parser = optparse.OptionParser(
        usage="%prog cement-helper [options] [project name] [helper_name]",
        version="%prog " + version
        )
    parser.add_option("-t", "--templates",
        help="user specific templates",
        dest="templates", default=templates
        )
    parser.add_option("--dry-run",
        help="dry run (don't actually do anything)",
        action="store_true", dest="dry_run"
        )
    
    def command(self):
        """LayCement for the new project helper."""
        
        self.__dict__.update(self.options.__dict__)
        
        if self.args:
            self.project = self.args[0].lower()
            self.helper = self.args[1].lower()
        
        while not self.project:
            self.project = raw_input("Enter project name: ").lower()
        while not self.helper:
            self.helper = raw_input("Enter helper name: ").lower()
            
        package = "%s-helpers-%s" % (self.project, self.helper)
        package = beginning_letter.sub("", package)
        package = valid_only.sub("_", package)
        if package:
            self.package = package
        else:
            self.package = None
            while not self.package:
                self.package = raw_input(
                    "Enter package name [%s]: " % package).strip() or package
        
        self.name = pkg_resources.safe_name(self.package)
    
        env = pkg_resources.Environment()
        if self.name.lower() in env:
            print 'The name "%s" is already in use by' % self.name,
            for dist in env[self.name]:
                print dist
                return

        import imp
        try:
            if imp.find_module(self.package):
                print 'The package name "%s" is already in use' % self.package
                return
        except ImportError:
            pass

        if os.path.exists(self.name):
            print 'A directory called "%s" already exists. Exiting.' % self.name
            return
        
        command = create_distro.CreateDistroCommand("create")
        cmd_args = []
        for template in self.templates.split():
            cmd_args.append("--template=%s" % template)
        cmd_args.append(self.name)
        cmd_args.append("project=%s" % self.project)
        cmd_args.append("helper=%s" % self.helper)
        cmd_args.append("cement_version=%s" % CEMENT_VERSION)
        cmd_args.append("cement__next_version=%s" % CEMENT_NEXT_VERSION)
        command.run(cmd_args)
        
        if not self.dry_run:
            sys.argv = ["setup.py", "egg_info"]
            
            # dirty hack to allow "empty" dirs
            for base, path, files in os.walk("./"):
                for file in files:
                    if file == "empty":
                        os.remove(os.path.join(base, file))                                                