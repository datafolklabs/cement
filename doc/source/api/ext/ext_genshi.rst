.. _cement.ext.ext_genshi:

:mod:`cement.ext.ext_genshi`
----------------------------

.. automodule:: cement.ext.ext_genshi
    :members:   
    :private-members:
    :show-inheritance:

Genshi Syntax Basics
^^^^^^^^^^^^^^^^^^^^

**Printing Variables**

.. code-block:: text

    Hello ${user_name}


Where ``user_name`` is a variable returned from the controller.  Will display:

.. code-block:: text

    Hello Johnny


**Conditional Statements**

.. code-block:: text

    {% if foo %}\\
    Label: ${example.label}
    {% end %}\\


Will only output ``Label: <label>`` if ``foo == True``.

**For Loops**

.. code-block:: text

    {% for item in items %}\\
      - ${item}
    {% end %}\\


Where ``items`` is a list returned from the controller.  Will display:

.. code-block:: text

     - list item 1
     - list item 2
     - list item 3


**Functions**

.. code-block:: text

    {% def greeting(name) %}\\
    Hello, ${name}!
    {% end %}\\

    ${greeting('World')}\\
    ${greeting('Edward')}


Will output:

.. code-block:: text

    Hello, World!
    Hello, Edward!


**Formatted Columns**

.. code-block:: text

    {# --------------------- 78 character baseline --------------------------- #}\\

    label               ver       description
    ==================  ========  ================================================
    {% for plugin in plugins %}\\
    ${"%-18s" % plugin['label']}  ${"%-8s" % plugin['version']}  ${"%-48s" % plugin['description']}
    {% end %}


Output looks like:

.. code-block:: text

    $ helloworld list-plugins

    label               ver       description
    ==================  ========  ================================================
    example1            1.0.34    Example plugin v1.x for helloworld
    example2            2.1       Example plugin v2.x for helloworld