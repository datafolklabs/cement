# ChangeLog

## 3.0.10 - Feb 28, 2024

Bugs: 

- `[ext.logging]` Support `logging.propagate` to avoid duplicate log entries
    - [Issue #310](https://github.com/datafolklabs/cement/issues/310)
- `[core.foundation]` Quiet mode file is never closed
    - [Issue #653](https://github.com/datafolklabs/cement/issues/653)
- `[ext.smtp]` Ability to Enable TLS without SSL
    - [Issue #667](https://github.com/datafolklabs/cement/issues/667)
- `[ext.smtp]` Empty (wrong) addresses sent when CC/BCC is `None`
    - [Issue #668](https://github.com/datafolklabs/cement/issues/668)


Features:

- `[utils.fs]` Add Timestamp Support to fs.backup
    - [Issue #611](https://github.com/datafolklabs/cement/issues/611)
- `[ext.smtp]` Support for sending file attachements.
    - [PR #669](https://github.com/datafolklabs/cement/pull/669)
- `[ext.smtp]` Support for sending both Plain Text and HTML
    - [PR #669](https://github.com/datafolklabs/cement/pull/669)


Refactoring: 

- `[core.plugin]` Deprecate the use of `imp` in favor of `importlib`
    - [Issue #386](https://github.com/datafolklabs/cement/issues/386)
- `[ext.smtp]` Actually test SMTP against a real server (replace mocks)


Misc:

- `[dev]` Add Smoke tests for Python 3.11, 3.12
- `[dev]` Make Python 3.12 the default development target
- `[dev]` Drop support for Python 3.7
    - [Issue #658](https://github.com/datafolklabs/cement/issues/658)
- `[docker]` Base official Docker image on Python 3.12
- `[utils.version]` Resolve deprecated `datetime.utcfromtimestamp()`
    - [Issue #661](https://github.com/datafolklabs/cement/issues/661)
- `[dev]` Add `comply-typing` to make helpers, start working toward typing.
    - [Issue #599](https://github.com/datafolklabs/cement/issues/661)
    - [PR #628](https://github.com/datafolklabs/cement/pull/628)
- `[dev]` Add `mailpit` service to docker-compose development config.

Deprecations:

- `[ext.logging]` Deprecate FATAL facility in favor of CRITICAL.
    - [Issue #533](https://github.com/datafolklabs/cement/issues/533)


## 3.0.8 - Aug 18, 2022

Bugs:

- `[cli]` Cement CLI broken on Python 3.10
    - [Issue #619](https://github.com/datafolklabs/cement/issues/619)
- `[cli]` Generated script returns version of Cement
    - [Issue #632](https://github.com/datafolklabs/cement/issues/632)
- `[cli]` Generated script should allow dash/underscore
    - [Issue #614](https://github.com/datafolklabs/cement/issues/614)
- `[core.foundation]` App.render() not suppressed in quiet mode
    - [Issue #636](https://github.com/datafolklabs/cement/issues/636)
- `[core.foundation]` Console log not suppressed by output handler override (JSON/YAML)
    - [Issue #637](https://github.com/datafolklabs/cement/issues/637)


Features:

- `[utils.shell]` Support `suppress` meta option on `Prompt` to suppress user input.
    - [Issue #621](https://github.com/datafolklabs/cement/issues/621)
- `[ext]` Use `extras_require` for optional extensions
    - [Issue #604](https://github.com/datafolklabs/cement/issues/604)

Refactoring:

- `[utils.misc]` Use SHA256 instead of MD5 in `rando()` to support Redhap/FIPS compliance
    - [Issue #626](https://github.com/datafolklabs/cement/issues/626)
- `[core.foundation]` Make quiet/debug options configurable
    - [Issue #613](https://github.com/datafolklabs/cement/issues/613)

Misc:

- `[dev]` Cement CLI smoke tests
    - [Issue #620](https://github.com/datafolklabs/cement/issues/620)
- `[dev]` Add Python 3.10 to Travis CI tests
    - [Issue #618](https://github.com/datafolklabs/cement/issues/618)
- `[core.deprecations]` Implement Cement deprecation warnings
    - [Issue #631](https://github.com/datafolklabs/cement/issues/631)


Deprecations:

- `[core.foundation]` Deprecate CEMENT_FRAMEWORK_LOGGING in favor of CEMENT_LOG.
    - [Issue #638](https://github.com/datafolklabs/cement/issues/638)


## 3.0.6 - Dec 18, 2021

Bugs:

- `[ext.argparse]` Parser (`self._parser`) not accessible inside `_pre_argument_parsing` when `stacked_type = 'embedded'`
    - [Issue #569](https://github.com/datafolklabs/cement/issues/569)
- `[ext.configparser]` Overriding config options with environment variables doesn't work correctly with surrounding underscore characters 
    - [Issue #590](https://github.com/datafolklabs/cement/issues/590)
- `[utils.fs]` Fix bug where trailing slash was not removed in `fs.backup()` of a directory.
    - [Issue #610](https://github.com/datafolklabs/cement/issues/610)
- `[cement.cli]` Generated README contains incorrect installation instructions.
    - [Issue #588](https://github.com/datafolklabs/cement/issues/588)

Features:

- None


Refactoring:

- `[ext.colorlog]` Support subclassing of ext_colorlog.
    - [Issue #571](https://github.com/datafolklabs/cement/issues/571)


Misc:

- `[dev]` Update to Python 3.10 for default development / Docker version.
- `[dev]` Remove Python 3.5/3.6 from Travis CI tests.


## 3.0.4 - May 17, 2019

Bugs:

- `[ext.yaml]` YamlConfigHandler uses unsafe load method
   - [Issue #553](https://github.com/datafolklabs/cement/issues/553)
- `[ext.configparser]` Configparser 'getboolean' exception
   - [Issue #558](https://github.com/datafolklabs/cement/issues/558)


Features:

- `[utils.misc]` Support `y` as a truth boolean in `utils.misc.is_true`
    - [Issue #542](https://github.com/datafolklabs/cement/issues/542)


## 3.0.2 - November 6, 2018

Bugs:

- `[cli]` Generate Variable Mishap in Project Template
    - [Issue #532](https://github.com/datafolklabs/cement/issues/532)
- `[ext.generator]` Error class is malformed
    - [Issue #535](https://github.com/datafolklabs/cement/issues/535)
- `[core.template]` MemoryError during 'cement generate project'
    - [Issue #531](https://github.com/datafolklabs/cement/issues/531)
- `[core.foundation]` Contents of plugin_dirs is printed to console
    - [Issue #538](https://github.com/datafolklabs/cement/issues/538)


Features:

- `[ext.argparse]` Command name override
    - [Issue #529](https://github.com/datafolklabs/cement/issues/529)


## 3.0.0 - August 21, 2018

Bugs:

- `[ext.redis]` Unable To Set Redis Host
    - [Issue #440](https://github.com/datafolklabs/cement/issues/440)
- `[ext.argparse]` Empty Sub-Commands List
    - [Issue #444](https://github.com/datafolklabs/cement/issues/444)
- `[core.foundation]` Handler Override Options Do Not Honor Meta Defaults
    - [Issue #513](https://github.com/datafolklabs/cement/issues/513)

Features:

- `[core]` Add Docker / Docker Compose Support
    - [Issue #439](https://github.com/datafolklabs/cement/issues/439)
- `[core]` Add ability to override the output handler used when `app.render()` is called.
    - [Issue #471](https://github.com/datafolklabs/cement/issues/471)
- `[ext.print]` Add the Print Extension to be used as a drop in replacement for the standard ``print()``, but allowing the developer to honor framework features like `pre_render` and `post_render` hooks.
- `[ext.scrub]` Add Scrub Extension to easily obfuscate sensitive data from rendered output.
    - [Issue #469](https://github.com/datafolklabs/cement/issues/469)
- `[core]` Add ability to override config settings via environment variables.
    - [Issue #437](https://github.com/datafolklabs/cement/issues/437)
- `[ext.argparse]` Add ability to get list of exposed commands
    - [Issue #455](https://github.com/datafolklabs/cement/issues/455)
- `[core]` Add Template Interface
    - [Issue #464](https://github.com/datafolklabs/cement/issues/464)
- `[ext.mustache]` Add MustacheTemplateHandler
- `[ext.handlebars]` Add HandlebarsTemplateHandler
- `[ext.jinja2]` Add Jinja2TemplateHandler
- `[ext.generate]` Add Generate Extension
    - [Issue #487](https://github.com/datafolklabs/cement/issues/487)
- `[ext.logging]` Add `-l LEVEL` command line option to override log level
    - [Issue #497](https://github.com/datafolklabs/cement/issues/497)
- `[cli]` Add Cement CLI (includes ability to generate apps, plugins,
    extensions, and scripts using the Generate Extension)
    - [Issue #490](https://github.com/datafolklabs/cement/issues/490)
- `[core]` Added clear separation between Interfaces and Handlers
    - [Issue #506](https://github.com/datafolklabs/cement/issues/506)
- `[utils.fs]` - Added several helpers include `fs.Tmp` for creation and cleanup of temporary directory and file.

Refactoring:

- *Too many to reference*


Incompatible:

- `[core]` Replace Interfaces with ABC Base Classes
    - [Issue #192](https://github.com/datafolklabs/cement/issues/192)
- `[core.foundation]` Rename `CementApp` to `App`.
- `[core.foundation]` Drop deprecated `App.Meta.override_arguments`
- `[core.foundation]` Remove `App.Meta.plugin_config_dir` and `App.Meta.plugin_config_dirs` in favor of `App.Meta.config_dirs`
    - [Issue #521](https://github.com/datafolklabs/cement/issues/521)
- `[core.founcation]` Rename `App.Meta.plugin_bootstrap` as `App.Meta.plugin_module`
    - [Issue #523](https://github.com/datafolklabs/cement/issues/523)
- `[core.handler]` Rename `CementBaseHandler` to `Handler`
- `[core.handler]` Drop deprecated backend globals
- `[core.hook]` Drop deprecated backend globals
- `[core.controller]` Drop `CementBaseController`
- `[ext.logging]` Drop deprecated `warn` facility (use `warning`)
- `[ext.argcomplete]` Drop ArgComplete Extension
- `[ext.reload_config]` Drop Reload Config Extension
- `[ext.configobj]` Drop ConfigObj Extension
- `[ext.json]` Disable `overridable` option by default
- `[ext.yaml]` Disable `overridable` option by default
- `[ext.json_configobj]` Drop JSON ConfigObj Extension
- `[ext.yaml_configobj]` Drop YAML ConfigObj Extension
- `[ext.handlebars]` Drop Handlebars Extension
- `[ext.genshi]` Drop Genshi Extension
- `[ext.argparse]` `ArgparseController.Meta.default_func` is now `_default`, and will print help info and exit.  Can now set this to `None` as well to pass/exit.
    - [Issue #426](https://github.com/datafolklabs/cement/issues/426)
- `[ext.plugin]` All plugin configuration sections must start with `plugin.`.
    For example, `[plugin.myplugin]`.
- `[core.foundation]` Renamed `App.Meta.config_extension` to `App.Meta.config_file_suffix`
    - [Issue #445](https://github.com/datafolklabs/cement/issues/445)
- `[core.foundation]` Drop `App.Meta.arguments_override_config`
    - [Issue #493](https://github.com/datafolklabs/cement/issues/493)

Deprecation:

- *Everything with deprecation notices in Cement < 3*
