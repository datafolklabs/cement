# Cement Contribution Guidelines

Cement is an open-source project, and is open to any and all contributions that other developers would like to provide. This document provides some guidelines that all contributors must be aware of, and abide by to have their submissions included in the source.

## Licensing

The Cement source code is licensed under the BSD three-clause license and is approved by the [Open Source Initiative]. All contributed source code must be either the original work of the contributing author, which will be contributed under the BSD license, or work taken from another project that is released under a BSD-compatible license.

## Submitting Bug Reports and Feature Requests

If you've found a bug, or would like to request a feature please create a detailed issue in the [issue tracker].

The ideal bug report would include:

- Bug description
- Include the version of Python, Cement, and any dependencies in use
- Steps to reproduce the bug
- Code samples that show the bug in action
- A pull request including code that:
    1. Fixes the bug
    2. Has at least one test case that tests for the bug specifically

The ideal feature request would include:

- Feature description
- Example code, or pseudo code of how you might use the feature
- Example command line session showing how the feature would be used by the end-user
- A pull request including:
    - The feature you would like added
    - At least one test case that tests the feature and maintains 100% code coverage when tests are run (meaning that your tests should cover 100% of your contributed code)
    - Documentation that outlines how to use the feature

## Guidelines for Code Contributions

All contributors should attempt to abide by the following:

- Contributors fork the project on GitHub onto their own account
- All changes should be commited, and pushed to their repository
- All pull requests are from a topic branch, not an existing Cement branch
- Contributors make every effort to comply with [PEP8]
- Before starting on a new feature, or bug fix, always do the following:
    - `git pull --rebase` to get latest changes from upstream
    - Checkout a new branch.  For example:
        - `git checkout -b feature/slug-name`
        - `git checkout -b bug/github-issue-number`
- Code must include the following:
    - All tests pass successfully
    - Coverage reports 100% code coverage when running tests
    - New features are documented in the appropriate section of the doc
    - Significant changes are mentioned in the ChangeLog
- All contributions must be associated with at least one issue in GitHub.  If the issue does not exist, create one (per the guidelines above).
- Commit comments must include something like the following:
    - Resolves Issue #1127
    - Partially Resolves Issue #9873
- A single commit per issue.
- Contributors should add their full name, or handle, to the CONTRIBUTORS file.

Regarding git commit messages, please read the following:

* [Commit Guidelines]

The majority of commits only require a single line commit message.  That said, for more complex commits, please use the following as an example (as outlined in the ProGit link above):

```
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
```

[Open Source Initiative]: http://www.opensource.org
[issue tracker]: http://github.com/datafolklabs/cement/issues
[PEP8]: http://www.python.org/dev/peps/pep-0008/
[Commit Guidelines]: http://git-scm.com/book/en/Distributed-Git-Contributing-to-a-Project#Commit-Guidelines
