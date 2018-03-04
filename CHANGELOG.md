# ChangeLog

## 2.99.1 - DEVELOPMENT (will be released as dev/2.99.2 or stable/3.0.0)

This is a complete fork from Cement 2 code base.  Please continue to use
stable versions of Cement 2, until Cement 3.0.0 is released.


Bugs:

- `[ext.redis]` Unable To Set Redis Host
    - [Issue #440](https://github.com/datafolklabs/cement/issues/440)
- `[ext.argparse]` Empty Sub-Commands List
    - [Issue #444](https://github.com/datafolklabs/cement/issues/444)


Features:

- `[core]` Add Docker / Docker Compose Support
    - [Issue #439](https://github.com/datafolklabs/cement/issues/439)
- `[core]` Add ability to override the output handler used when `app.render()`
  is called.
    - [Issue #471](https://github.com/datafolklabs/cement/issues/471)
- `[ext.print]` Added the Print Extension to be used as a drop in replacement
  for the standard ``print()``, but allowing the developer to honor framework
  features like `pre_render` and `post_render` hooks.
- `[ext.scrub]` Added Scrub Extension to easily obfuscate sensitive data from
  rendered output.
    - [Issue #469](https://github.com/datafolklabs/cement/issues/469)
- `[core]` Add ability to override config settings via envirionment variables.
    - [Issue #437](https://github.com/datafolklabs/cement/issues/437)


Refactoring:

- *Too many to reference*


Incompatible:

- `[core]` Replace Interfaces with ABC Base Classes
    - [Issue #192](https://github.com/datafolklabs/cement/issues/192)
- `[core.foundation]` Rename `CementApp` to `App`.
- `[core.handler]` Rename `CementBaseHandler` to `Handler`
- `[core.handler]` Drop deprecated backend globals
- `[core.hook]` Drop deprecated backend globals
- `[core.controller]` Drop `CementBaseController`
- `[ext.argcomplete]` No longer shipped with Cement.
- `[ext.reload_config]` No longer shipped with Cement.
- `[ext.configobj]` No longer shipped with Cement.
- `[ext.json_configobj]` No longer shipped with Cement.
- `[ext.yaml_configobj]` No longer shipped with Cement.
- `[ext.genshi]` No longer shipped with Cement.
- `[ext.argparse]` ArgparseController.Meta.default_func is not `_default`, and
  will print help info and exit.  Can now set this to `None` as well to
  pass/exit.
    - [Issue #426](https://github.com/datafolklabs/cement/issues/426)
- `[ext.plugin]` All plugin configuration sections must start with `plugin.`.
    For example, `[plugin.myplugin]`.
- `[core.foundation]` Renamed `App.Meta.config_extension` to
    `App.Meta.config_file_suffix`
    - [Issue #445](https://github.com/datafolklabs/cement/issues/445)


Deprecation:

- *Everything with deprecation notices in Cement < 3*
