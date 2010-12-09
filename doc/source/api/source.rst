A Look at The Source Code
=========================

All source 'packages' are available under the './src' directory.  There are
the following python packages:

    ./src/cement.core/
        This package provides the core framework required to run an 
        application built on top of Cement.
        
    ./src/cement.devtools/
        This package provides development tools for creating and developing
        applications built on Cement.
        
    ./src/cement.test/
        This package provides an external application, built on top of 
        Cement, that also provides the nose tests to run and test the 
        framework. Testing requires a 'running' application to really cover
        all bits of the framework code, and this is that 'running' 
        application.
    
    
Additional directories include:

    ./doc/
        Sphinx documentation (what you're reading now).
    
    ./util/
        Utilities/scripts/etc that help with development of Cement.
