"""
Paste commands to a generate a new Cement projects and plugins.

Create a new project named helloworld with this command:

    $ paster laycement helloworld
    
    
Create a new plugin for the helloworld project with this command:

    $ paster laycement helloworld -p myplugin


Usage:

.. parsed-literal::

    paster laycement [--version][-h|--help]
            [-p PLUGIN][--dry-run][-t|--template TEMPLATE]

.. container:: paster-usage

  --version
      show program's version number and exit
  -h, --help
      show this help message and exit
  -p PLUGIN, --plugin=PLUGIN
      plugin name for the code
  --dry-run
      dry run (don't actually do anything)
  -t TEMPLATE, --template=TEMPLATE
      user specific template
    
"""

import sys, os
import re
import pkg_resources
import optparse
from paste.script import command
from paste.script import create_distro

beginning_letter = re.compile(r"^[^a-z]*")
valid_only = re.compile(r"[^a-z0-9_]")

class LayCementCommand(command.Command):
    """Create a new CLI Application using the Cement Framework.

Example usage::

    $ paster laycement yourproject
    """
    version = pkg_resources.get_distribution('cement').version
    summary = __doc__.splitlines()[0]
    usage = '\n' + __doc__
    name = None
    group_name = "Cement"
    dry_run = False
    templates = "cement"
    
    parser = command.Command.standard_parser(quiet=True)
    parser = optparse.OptionParser(
        usage="%prog laycement [options] [project name]",
        version="%prog " + version
        )
    parser.add_option("-p", "--plugin",
        help="plugin name to add to [project_name]",
        dest="plugin"
        )
    parser.add_option("-e", "--ext-plugin",
        help="external plugin name to add for [project_name]",
        dest="ext_plugin"
        )
    parser.add_option("-t", "--templates",
        help="user specific templates",
        dest="templates"
        )
    parser.add_option("--dry-run",
        help="dry run (don't actually do anything)",
        action="store_true", dest="dry_run"
        )
    
    def command(self):
        """LayCement for the new project."""
        
        if self.args:
            self.name = self.args[0]

        while not self.name:
            self.name = raw_input("Enter project name: ")
            
        package = self.name.lower()
        package = beginning_letter.sub("", package)
        package = valid_only.sub("", package)
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
        
        command.run(cmd_args)
        
        if not self.dry_run:
            sys.argv = ["setup.py", "egg_info"]
            #import imp
            #imp.load_module("setup", *imp.find_module("setup", ["."]))
            
            # dirty hack to allow "empty" dirs
            for base, path, files in os.walk("./"):
                for file in files:
                    if file == "empty":
                        os.remove(os.path.join(base, file))