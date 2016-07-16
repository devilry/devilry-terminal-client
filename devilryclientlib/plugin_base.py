import argparse


class PluginBase(object):
    """
    This is a base plugin class.

    When creating a plugin subclass this class.
    It's important to set plugin equal to your new plugin class

    Examples:
        class Plugin(PluginBase):

            @classmethod
            def description(cls):
                return 'some description'

        plugin = Plugin

    """

    def __init__(self):
        self.parser = argparse.ArgumentParser(description=self.description())

    def query_parser(self, dict):
        query = ''
        for key, value in dict.items():
            query += '&{}={}'.format(key, value)
        return '?{}'.format(query[1:])

    def run(self):
        raise NotImplementedError

    @classmethod
    def description(cls):
        raise NotImplementedError
