Versioning and Compatibility
----------------------------

This outline uses fictitious version numbers to avoid confusion between 
actual releases and this doc. Cement is versioned as follows, using the 
version 0.2.4 as the example:

 * 0 = Code Base
 * 2 = Major Release Version
 * 4 = Minor Release Version

That said, the Major Release Version and the Minor Release Version both 
honor the following scheme:

 * Even = Stable
 * Odd = Development

Therefore, if 0.2.4 (even, even) is the current stable release of the '0' 
branch, then 0.2.5 (even, odd) is the 'in progress' version in the Git 
'master' branch. Once 0.2.5 reaches releasability it would be released as 
0.4.6 stable (even, even).

Development versions also follow the same scheme.  The next major release
that breaks API compatibility would be versioned as 0.3.1 (odd, odd).  Once a
'stable enough' version of the development branch reaches releasability, it 
will be released as 0.3.2 (odd, even) meaning the branch is development, but 
it is a semi-stable release.
    
Any time API compatibility changes we will up the Major Release Version. We 
handle this in setup.py of Cement applications by doing something like:

.. code-block:: python

    install_requires=[
        "cement.core >=0.2.4, <0.3"
        ]

This means, if you write an application on top of cement == 0.2.4 then your 
application should be compatible with all versions of 0.2.x, however would not 
be compatible with anything >=0.3 because 0.3 is the next development version
where API compatibility changes.  For that reason the next major development 
branch is 0.3 (odd) currently, and the next major stable branch of cement will 
be 0.4 (even).  Both 0.3 (development) and 0.4 (stable) break compatibility 
with previous versions of Cement < 0.3.

The 'Code Base' version more or less designates a 'full rewrite'.  Meaning
that within the same code base (i.e. '0') even in the next major version that
break compatibility, you should be able to make your application work with
only a few changes.  Where as, in the next code base (i.e. 1) it is likely 
that you will need to make significant changes, or possibly rewrite your
application to work on the newer code base.

To keep API compatible, and non compatible development separate we work out of 
two Git repos.

 * master: development that is API compatible with current stable.
 * portland: development that is API incompatible with current stable.
