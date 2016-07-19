import argparse

from requests.exceptions import HTTPError

from api_client.client import Client
from devilryclientlib.plugin import BaseApiPlugin


class Assignment(BaseApiPlugin):
    queryparams = ['ordering', 'search', 'subject', 'semester']

    def __init__(self):
        super(Assignment, self).__init__()
        self.core_parser()
        self.list_arguments()

    @classmethod
    def description(cls):
        return 'Assignment list/get'

    def run(self, args):
        args = self.parser.parse_args(args)
        args.func(args)

    def core_parser(self):
        """
        Initialize the core parser
        """
        self.parser = argparse.ArgumentParser(description=self.description(), prog='devil assignment')
        self.subparsers = self.parser.add_subparsers(help='Commands')

    def common_arguments(self, parser):
        """
        Adds common arguments to the passed parser
        """
        parser.add_argument('-k', '--key', help='Your api key', dest='key', default=None)
        parser.add_argument('-r', '--role', dest='role',
                            required=True, help='Choose role: student, examiner, admin',
                            choices=['student', 'examiner', 'admin'])

    def list_arguments(self):
        """
        arguments for the subparser list
        """
        self.list_parser = self.subparsers.add_parser('list', help='list assignments')
        self.common_arguments(self.list_parser)
        self.list_parser.add_argument('-q', '--query-string', dest='query_string',
                                      help='query string \"?id=2&order=name\"')
        self.list_parser.add_argument('-o', '--ordering', dest='ordering',
                                      choices=['publishing_date', 'publishing_time', 'short_name',
                                               '-publishing_date', '-publishing_time', '-short_name'], default=None,
                                      help='Choose order, \'-\' prefix for descending order')
        self.list_parser.add_argument('-s', '--search', dest='search', help='search field(semester, subject)', default=None)
        self.list_parser.add_argument('--subject', dest='subject', help='filter subject', default=None)
        self.list_parser.add_argument('--semester', dest='semester', help='filter semester', default=None)
        self.list_parser.set_defaults(func=self.list)

    def list(self, args):
        """
        If the subparser list is being used this function is called.
        """
        client = Client(self.url)
        client.auth(args.key)
        try:
            api = client.api('student/assignment/list')
            self.list_prettyprint(api.get().json())
        except HTTPError as e:
            print(e)

plugin = Assignment
