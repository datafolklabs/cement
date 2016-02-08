BASH Auto Completion
--------------------

Auto Completion, or "TAB Completion" is a very common and familiar feature in
BASH (and other modern shells).  It is possible to auto-complete Cement apps
(using BASH for this example) including sub-levels for nested controllers.
The difficulty is that this auto-completion code must be maintained outside of
Cement and your application code, and be implemented in the shell environment
generally by use of an "RC" file, or similar means.  This then must be updated
anytime your application is modified (or atleast any time the
sub-commands/controllers/arguments are modified).

Note that, in the future, we would love to include some form of
"BASH RC Generator" that will do this for you, however in the meantime the
following is a working example that can be used as a model for adding BASH
auto-completion to your app.

Update: As of Cement 2.7.x, the 
:ref:`Argcomplete Framework Extension<cement.ext.ext_argcomplete>` can be 
used as an alternative to this example.  Both are viable options though
this route is much more manual, and the Argcomplete route might not fit your 
needs.

Example Cement App
^^^^^^^^^^^^^^^^^^

The following application code implements three levels of namespaces, or
sub-commands, that are implemented via nested-controllers.

.. code-block:: python

    from cement.core.foundation import CementApp
    from cement.core.controller import CementBaseController, expose

    class BaseController(CementBaseController):
        class Meta:
            label = 'base'

        @expose()
        def base_cmd1(self):
            print("Inside BaseController.base_cmd1()")

    class EmbeddedController(CementBaseController):
        class Meta:
            label = 'embedded'
            description = "embedded with base namespace"
            stacked_on = 'base'
            stacked_type = 'embedded'

        @expose()
        def base_cmd2(self):
            print("Inside EmbeddedController.base_cmd2()")

        @expose()
        def embedded_cmd3(self):
            print("Inside EmbeddedController.embedded_cmd3()")

    class SecondLevelController(CementBaseController):
        class Meta:
            label = 'second'
            description = ''
            stacked_on = 'base'
            stacked_type = 'nested'

        @expose()
        def second_cmd4(self):
            print("Inside SecondLevelController.second_cmd4()")

        @expose()
        def second_cmd5(self):
            print("Inside SecondLevelController.second_cmd5()")

    class ThirdLevelController(CementBaseController):
        class Meta:
            label = 'third'
            description = ''
            stacked_on = 'second'
            stacked_type = 'nested'

        @expose()
        def third_cmd6(self):
            print("Inside ThirdLevelController.third_cmd6()")

        @expose()
        def third_cmd7(self):
            print("Inside ThirdLevelController.third_cmd7()")


    class MyApp(CementApp):
        class Meta:
            label = 'myapp'
            handlers = [
                BaseController,
                EmbeddedController,
                SecondLevelController,
                ThirdLevelController,
                ]


    def main():
        with MyApp() as app:
            app.run()

    if __name__ == '__main__':
        main()

This looks like:

.. code-block:: bash

    $ python myapp.py --help
    usage: myapp.py (sub-commands ...) [options ...] {arguments ...}

    Base Controller

    commands:

      base-cmd1

      base-cmd2

      embedded-cmd3

      second


    $ python myapp.py second --help

    commands:

      second-cmd4

      second-cmd5

      third


    $ python myapp.py second third --help

    commands:

      third-cmd6

      third-cmd7



For demonstration purposes, we are going to create a BASH alias here so that
we can call our `myapp` command name as if we would in production (not
development):

.. code-block:: bash

    $ alias myapp="python ./myapp.py"


In the "real world" your actual `myapp` command would be setup/installed by
something like this in `setup.py`:

.. code-block:: python

    entry_points="""
        [console_scripts]
        myapp = myapp.cli.main:main
        """,


Or by simply copying `myapp.py` to `/usr/bin/myapp`, or similar.

Example BASH RC
^^^^^^^^^^^^^^^

The following is a BASH RC script that will setup auto-completiong for the
above Cement App `myapp`.  You **will** need to modify this, it is just an
example and is not intended to be copy and pasted:

.. code-block:: bash

    alias myapp="python ./myapp.py"

    _myapp_complete()
    {
        local cur prev BASE_LEVEL

        COMPREPLY=()
        cur=${COMP_WORDS[COMP_CWORD]}
        prev=${COMP_WORDS[COMP_CWORD-1]}

        # SETUP THE BASE LEVEL (everything after "myapp")
        if [ $COMP_CWORD -eq 1 ]; then
            COMPREPLY=( $(compgen \
                          -W "base-cmd1 base-cmd2 embedded-cmd3 second" \
                          -- $cur) )


        # SETUP THE SECOND LEVEL (EVERYTHING AFTER "myapp second")
        elif [ $COMP_CWORD -eq 2 ]; then
            case "$prev" in

                # HANDLE EVERYTHING AFTER THE SECOND LEVEL NAMESPACE
                "second")
                    COMPREPLY=( $(compgen \
                                  -W "second-cmd4 second-cmd5 third" \
                                  -- $cur) )
                    ;;

                # IF YOU HAD ANOTHER CONTROLLER, YOU'D HANDLE THAT HERE
                "some-other-controller")
                    COMPREPLY=( $(compgen \
                                  -W "some-other-sub-command" \
                                  -- $cur) )
                    ;;

                # EVERYTHING ELSE
                *)
                    ;;
            esac

        # SETUP THE THIRD LEVEL (EVERYTHING AFTER "myapp second third")
        elif [ $COMP_CWORD -eq 3 ]; then
            case "$prev" in
                # HANDLE EVERYTHING AFTER THE THIRD LEVEL NAMESPACE
                "third")
                    COMPREPLY=( $(compgen \
                                  -W "third-cmd6 third-cmd7" \
                                  -- $cur) )
                    ;;

                # IF YOU HAD ANOTHER CONTROLLER, YOU'D HANDLE THAT HERE
                "some-other-controller")
                    COMPREPLY=( $(compgen \
                                  -W "some-other-sub-command" \
                                  -- $cur) )
                    ;;

                *)
                    ;;
            esac
        fi

        return 0

    } &&
    complete -F _myapp_complete myapp



You would then "source" the RC file:

.. code-block:: bash

    $ source myapp.rc


In the "real world" you would probably put this in a system wide location
such at ``/etc/profile.d`` or similar (in a production deployment).

Finally, this is what it looks like:

.. code-block:: bash

    # show all sub-commands at the base level
    $ myapp [tab] [tab]
    base-cmd1      base-cmd2      embedded-cmd3      second

    # auto-complete a partial matching sub-command
    $ myapp base [tab]

    $ myapp base-cmd [tab] [tab]
    base-cmd1      base-cmd2

    # auto-complete a full matching sub-command
    $ myapp sec [tab]

    $ myapp second

    # show all sub-commands under the second namespace
    $ myapp second [tab] [tab]
    second-cmd4      second-cmd5      third

    # show all sub-commands under the third namespace
    $ myapp second third [tab] [tab]
    third-cmd6      third-cmd7

