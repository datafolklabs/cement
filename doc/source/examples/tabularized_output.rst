Tabularized Output
==================

Users familiar with MySQL, PGSQL, etc find comfort in table-based output
patterns.  For one it adds structure, and two generally makes things much 
more readable.  The folloiwing is an example of a simple app using the 
:ref:`Tabulate <cement.ext.ext_tabulate>` extension:

.. code-block:: python

    from cement.core.foundation import CementApp
    from cement.core.controller import expose, CementBaseController


    class MyController(CementBaseController):
        class Meta:
            label = 'base'

        @expose(hide=True)
        def default(self):
            headers=['NAME', 'AGE', 'ADDRESS']
            data=[
                ["Krystin Bartoletti", 47, "PSC 7591, Box 425, APO AP 68379"],
                ["Cris Hegan", 54, "322 Reubin Islands, Leylabury, NC 34388"],
                ["George Champlin", 25, "Unit 6559, Box 124, DPO AA 25518"],
                ]
            self.app.render(data, headers=headers)


    class MyApp(CementApp):
        class Meta:
            label = 'myapp'
            extensions = ['tabulate']
            output_handler = 'tabulate'
            handlers = [MyController]


    with MyApp() as app:
        app.run()
        

The output looks like:

.. code-block:: console 

    $ python myapp.py

    | NAME               |   AGE | ADDRESS                                 |
    |--------------------+-------+-----------------------------------------|
    | Krystin Bartoletti |    47 | PSC 7591, Box 425, APO AP 68379         |
    | Cris Hegan         |    54 | 322 Reubin Islands, Leylabury, NC 34388 |
    | George Champlin    |    25 | Unit 6559, Box 124, DPO AA 25518        |