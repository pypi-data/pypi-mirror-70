subc
====

This is a tiny library to help you write CLI applications with many
sub-commands.

Installation
------------

``pip install subc``

Use
---

Create your own command subclass for your application (optional, but
encouraged):


.. code:: python

    class MyCmd(subc.Command):
        pass

Then, write commands in your application which sub-class this:

.. code:: python

    class HelloWorld(MyCmd):
        name = 'hello-world'
        description = 'say hello'
        def run(self):
            print('hello world')

Finally, use your application-level subclass for creating the argument parser
and running your application:

.. code:: python

    def main():
        parser = argparse.ArgumentParser(description='a cool tool')
        MyCmd.add_commands(parser)
        args = parser.parse_args()
        args.func(args)

License
-------

This project is released under the Revised BSD license.  See ``LICENSE.txt`` for
details.
