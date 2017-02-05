---
weight: 100
title: ChangeLog
---

# ChangeLog

## 2.11.1 - DEVELOPMENT (will be released as dev/2.11.2 or stable/2.12.0)

<aside class="warning">
This is a branch off of the 2.10.x stable code base.  Maintenance releases for
2.10.x will happen under the stable/2.10.x git branch, while forward feature
development will happen as 2.11.x under the git master branch.
</aside>

Bugs:

  * `[ext.logging]` Removes deprecated `warn` from ILog 
      validator, in-favor of `warning`
    * Issue #397
  *  `[ext.daemon]` Can't get user in daemon extension
    * Issue #401 
  * `[core]` FrameworkError when reusing CementApp object
    * Issue #415

Features:

  * None

Refactoring:

  * `[tests]` Refactor dto comply with Flake8
    * Issue #378
  * `[ext.daemon]` Ability to daemonize without `--daemon`
    * Issue #418

Incompatible:

  * None

Deprecation:

  * None
