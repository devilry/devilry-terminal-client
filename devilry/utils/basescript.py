class BaseScript(object):
    """
    This is the base class for any external or local script and should be subclassed when creating scripts.

    Examples:
        class MyScript(BaseScript):

        command = 'my-script'

        @classmethod
        def add_to_supparser(cls, subparser):
            parser = subparser.add_parser(cls.command, help='my super cool script')
            parser.add_argument('--my-cool-argument', dest='my_arg', require=True)
            parser.set_defaults(func=MyScript.run)

        @classmethod
        def run(cls, args):
            ...


    """
    @property
    def command(cls):
        """str: should be the name of the command."""
        raise NotImplementedError('Please set name of command Example: command = \'some-command\'')

    @classmethod
    def add_to_subparser(cls, subparser):
        """
        Examples:
            def add_to_subparser(cls, subparser):
                parser = subparser.add_parser(cls.command, help='some help message')
                parser.add_argument(...
                parser.set_defaults(func=MyScript.run)
        Args:
            subparser: subparser passed by the main method.

        Raises:
            NotImplementedError

        """
        raise NotImplementedError('Please implement add_to_subparser function')

    @classmethod
    def run(cls, args):
        """
        run is called when the positional argument is the class command (see add_to_subparser).

        Args:
            args: arguments parsed by argparse

        Raises:
            NotImplementedError
        """
        raise NotImplementedError('Please implement run function')
