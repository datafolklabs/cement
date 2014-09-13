Contributing
============

Cement is an open-source project, and is open to any and all contributions
that other developers would like to provide.  This document provides some
guidelines that all contributors must be aware of, and abide by to have their
submissions included in the source.

Licensing
---------

The Cement source code is licensed under the BSD three-clause license and is
approved by the `Open Source Initiative <http://www.opensource.org>`_.  All
contributed source code must be either the original work of the contributing
author, which will be contributed under the BSD license, or work taken from
another project that is released under a BSD-compatible license.

Submitting Bug Reports and Feature Requests
-------------------------------------------

If you've found a bug, or would like to request a feature please create a
detailed issue for it at `<http://github.com/datafolklabs/cement/issues>`_.

The ideal bug report would include:

    * Bug description
    * Include the version of Python, Cement, and any dependencies in use
    * Steps to reproduce the bug
    * Code samples that show the bug in action
    * A pull request including code that a) fixes the bug, and b) atleast one
      test case that tests for the bug specifically


The ideal feature request would include:

    * Feature description
    * Example code, or pseudo code of how you might use the feature
    * Example command line session showing how the feature would be used by
      the end-user
    * A pull request including:
        * The feature you would like added
        * At least one test case that tests the feature and maintains 100%
          code coverage when tests are run (meaning that your tests should
          cover 100% of your contributed code)
        * Documentation that outlines how to use the feature



Guidelines for Code Contributions
---------------------------------

All contributors should attempt to abide by the following:

    * Contributors fork the project on GitHub onto their own account
    * All changes should be commited, and pushed to their repository
    * All pull requests are from a topic branch, not an existing Cement branch
    * Contributors make every effort to comply with
      `PEP8 <http://www.python.org/dev/peps/pep-0008/>`_
    * Before starting on a new feature, or bug fix, always do the following:
        * ``git pull --rebase`` to get latest changes from upstream
        * Checkout a new branch.  For example:
            * ``git checkout -b feature/<feature_name>``
            * ``git checkout -b bug/<bug_number>``
    * Code must include the following:
        * All tests pass successfully
        * Coverage reports 100% code coverage when running tests
        * New features are documented in the appropriate section of the doc
        * Significant changes are mentioned in the ChangeLog
    * All contributions must be associated with at least one issue in GitHub.
      If the issue does not exist, create one (per the guidelines above).
    * Commit comments must include something like the following:
        * Resolves Issue #1127
        * Partially Resolves Issue #9873
    * A single commit per issue.
    * Contributors should add their full name, or handle, to the CONTRIBUTORS
      file.

Regarding git commit messages, please read the following:

  * `Commit Guidelines <http://git-scm.com/book/en/Distributed-Git-Contributing-to-a-Project#Commit-Guidelines>`_

The majority of commits only require a single line commit message.
That said, for more complex commits, please use the following as an example
(as outlined in the ProGit link above):

.. code-block:: text

    Short (50 chars or less) summary of changes

    More detailed explanatory text, if necessary.  Wrap it to about 72
    characters or so.  In some contexts, the first line is treated as the
    subject of an email and the rest of the text as the body.  The blank
    line separating the summary from the body is critical (unless you omit
    the body entirely); tools like rebase can get confused if you run the
    two together.

    Further paragraphs come after blank lines.

     - Bullet points are okay, too

     - Typically a hyphen or asterisk is used for the bullet, preceded by a
       single space, with blank lines in between, but conventions vary here


Source Code and Versioning
--------------------------

One of the primary goals of Cement is stability in the source code.  For this
reason we maintain a number of different git branches for focused
development.

**Development Branches**

Active 'forward' development happens out of two branches:

    * master - Development for the next minor stable release.
    * portland - Development for the next major release.


Additionally, specific development branches might exist in the future for
larger releases that may require iterative 'release candidate' handling before
an official stable release.  These branches will have the format of:

    * dev/3.1.x
    * dev/3.3.x
    * dev/4.1.x
    * dev/4.3.x
    * etc

**Stable Branches**

    * stable/0.8.x
    * stable/1.0.x
    * stable/1.2.x
    * stable/2.0.x
    * stable/2.2.x
    * stable/3.0.x
    * stable/3.2.x
    * etc

There is a system for versioning that may seem complex, and needs some
explanation.  Version numbers are broken up into three parts:

    * <Major>.<Minor>.<Bugfix>

This means:

    * Major - The major version of the source code generally relates to
      extensive incompatible changes, or entire code base rewrites.
      Applications built on the '1.x.x' version of Cement will need to be
      completely rewritten for the '2.x.x' versions of Cement.
    * Minor - The minor version signifies the addition of new features.  It
      may also indicate minor incompatibilities with the previous stable
      version, but should be easily resolvable with minimal coding effort.
    * Bugfix - During the lifecycle of a stable release such as '2.2.x', the
      only updates should be bug and/or security related.  At times, minor
      features may be introduced during a 'bugfix' release but that should
      not happen often.

It should be noted that both the Minor, and Bugfix versions follow a
``even == stable``, and ``odd == development`` scheme.  Therefore,
the current version in git will always end in an 'odd number'.  For example,
if the current stable version is ``2.0.18``, then the version in
``stable/2.0.x`` would be ``2.0.19``.  That said, the ``master`` branch might
then be ``2.1.1`` which is the first version of the next minor release.
Bugfixes would get applied to both branches, however feature updates would
only be applied to ``master``. The next stable release would then be ``2.2.0``
and a new git branch of ``stable/2.2.x`` will be created.

The ``portland`` branch is always very forward looking, and will contain
significant (and likely broken) code changes.  It should never be used for
anything other than development and testing.



