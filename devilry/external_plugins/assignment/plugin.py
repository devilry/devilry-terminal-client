from devilry.utils.baseplugin import BasePlugin
from devilry.devilry_api.assignment import Assignment as AssignmentApi
from requests.exceptions import HTTPError
from devilry.utils import colorize


class Assignment(BasePlugin):
    
    command = 'assignment'

    @classmethod
    def add_to_subparser(cls, subparser):
        parser = subparser.add_parser(cls.command, help='devilry_api assignment')
        parser.add_argument('-k', '--key', dest='key', help='Api key', required=True)
        parser.add_argument('-r', '--role', dest='role', choices=['student', 'examiner'], required=True)
        parser.add_argument('-a', '--action', dest='action', choices=['list'])
        parser.add_argument('-o', '--ordering', dest='ordering',
                            choices=['publishing_date', 'publishing_time', 'short_name',
                                     '-publishing_date', '-publishing_time', '-short_name'],
                            default=None)
        parser.add_argument('-s', '--search', dest='search', help='search field(semester, subject)')
        parser.add_argument('--subject', dest='subject', help='filter subject')
        parser.add_argument('--semester', dest='semester', help='filter semester')
        parser.add_argument('--format', dest='foramt', choices=['json', 'pretty'], default='pretty')
        parser.set_defaults(func=Assignment.run)

    @classmethod
    def run(cls, args):
        try:
            api = AssignmentApi(args.key, role=args.role, action=args.action)
        except HTTPError as e:
            print(colorize.colored_text(e, colorize.COLOR_RED))
            raise SystemExit()
        if args.format == 'json':
            print(api.get_json())
        else:
            api.pretty_print()
