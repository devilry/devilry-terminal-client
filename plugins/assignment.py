from lib.plugin_base import PluginBase
from api_client.client import Client
from requests.exceptions import HTTPError


class Assignment(PluginBase):

    url = 'http://localhost:8000/api'

    def parse_arguments(self, args):
        self.parser.usage = 'devil assignment [-h] [-k KEY] -r {student,examiner,admin} [-q QUERY_STRING] [-l]'
        self.parser.add_argument('-k', '--key', help='Your api key', dest='key', default=None)
        self.parser.add_argument('-r', '--role', dest='role',
                                 required=True, help='Choose role: student, examiner, admin',
                                 choices=['student', 'examiner', 'admin'])
        self.parser.add_argument('-q', '--query-string', dest='query_string',
                                 help='query string \"?id=2&order=name\"')
        self.parser.add_argument('-l', '--list', dest='list', action='store_true',
                                 help='list assignments', default=False)
        self.parser.add_argument('-o', '--ordering', dest='ordering',
                                 choices=['publishing_date', 'publishing_time', 'short_name',
                                          '-publishing_date', '-publishing_time', '-short_name'], default=None,
                                 help='Choose order, \'-\' prefix for descending order')
        self.parser.add_argument('-s', '--search', dest='search', help='search field(semester, subject)', default=None)
        self.parser.add_argument('--subject', dest='subject', help='filter subject', default=None)
        self.parser.add_argument('--semester', dest='semester', help='filter semester', default=None)
        self.args = self.parser.parse_args(args)

    def __init__(self, args):
        super(Assignment, self).__init__()
        self.parse_arguments(args)
        self.run()

    @classmethod
    def description(cls):
        return 'list/get assignment'

    def parse_query_dict(self):
        dict = {}
        if self.args.ordering:
            dict['ordering'] = self.args.ordering
        if self.args.search:
            dict['search'] = self.args.search
        if self.args.subject:
            dict['subject'] = self.args.subject
        if self.args.semester:
            dict['semester'] = self.args.semester
        return dict

    def list(self):
        client = Client(self.url)
        client.auth(key=self.args.key)
        api = client.api('/student/assignment/list/', queryparms=self.query_parser(self.parse_query_dict()))
        try:
            print(api.get().content)
        except HTTPError as e:
            print(str(e))

    def run(self):
        if self.args.list:
            self.list()


plugin = Assignment
