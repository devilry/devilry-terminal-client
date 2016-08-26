from devilry.utils.basescript import BaseScript
from devilry.devilry_api.assignment import Assignment as AssignmentApi
from requests.exceptions import HTTPError
from devilry.utils import colorize


class Assignment(BaseScript):

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
        parser.add_argument('-s', '--search', dest='search', help='search field(semester, subject, assignment name)')
        parser.add_argument('--subject', dest='subject_short_name', help='filter subject')
        parser.add_argument('--semester', dest='period_short_name', help='filter semester')
        parser.add_argument('--assignment-name', dest='short_name', help='filter name of assignment')
        parser.add_argument('--id', dest='id', help='id of assignment')
        parser.add_argument('--format', dest='format', choices=['json', 'pretty'], default='pretty')
        parser.set_defaults(func=Assignment.run)

    @classmethod
    def run(cls, args):
        try:
            kwargs = dict(
                search=args.search,
                ordering=args.ordering,
                subject_short_name=args.subject_short_name,
                period_short_name=args.period_short_name,
                short_name=args.short_name,
                id=args.id
            )
            api = AssignmentApi(args.key, args.role, action=args.action, **kwargs)
        except HTTPError as e:
            print(colorize.colored_text(e, colorize.COLOR_RED))
            raise SystemExit()
        if args.format == 'json':
            print(api.get_json())
        else:
            api.pretty_print()
