from lib.plugin_base import PluginBase


class Assignment(PluginBase):

    def parse_arguments(self, args):
        self.parser.usage = 'devil assignment [-h] [-k KEY] -r {student,examiner,admin} [-q QUERY_STRING] [-l]'
        self.parser.add_argument('-k', '--key', help='Your api key', dest='key')
        self.parser.add_argument('-r', '--role', dest='role',
                                 required=True, help='Choose role: student, examiner, admin',
                                 choices=['student', 'examiner', 'admin'])
        self.parser.add_argument('-q', '--query-string', dest='query_string',
                                 help='query string \"?id=2&order=name\"')
        self.parser.add_argument('-l', '--list', dest='list', action='store_true',
                                 help='list assignments', default=False)
        self.args = self.parser.parse_args(args)

    def __init__(self, args):
        super(Assignment, self).__init__()
        self.parse_arguments(args)

    @classmethod
    def description(cls):
        return 'list/get assignment'


plugin = Assignment
