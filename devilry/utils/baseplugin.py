

class BasePlugin(object):

    @property
    def command(cls):
        raise NotImplementedError('Please set name of command Example: command = \'some-command\'')

    def add_to_subparser(cls, subparser):
        """
        Examples:
            def add_to_subparser(cls, subparser):
        Args:
            subparser: subparser

        Returns:

        """
        raise NotImplementedError('Please implement add_to_subparser function')

    def run(cls, args):
        """
        """
        raise NotImplementedError('Please implement run function')
