from devilry.utils.basescript import BaseScript
from devilry.devilry_api.assignmentGroup import AssignmentGroup as AssignmentGroupApi
from requests.exceptions import HTTPError
from devilry.utils import colorize


class AssignmentGroup(BaseScript):

    command = 'assignment-group'

    @classmethod
    def add_to_subparser(cls, subparser):
        parser = subparser.add_parser(cls.command, help='devilry_api assignment group')
        parser.add_argument('-k', '--key', dest='key', help='Api key', required=True)
        parser.add_argument('-r', '--role', dest='role', choices=['student', 'examiner'], required=True)
        parser.add_argument('-a', '--action', dest='action', choices=['list'])
        parser.add_argument('-o', '--ordering', dest='ordering',
                            choices=['id', 'is_corrected', 'assignment_short_name',
                                     '-id', '-is_corrected', '-assignment_short_name'],
                            default=None)
        parser.add_argument('-s', '--search', dest='search', help='search field(semester, subject, assignment name)')
        parser.add_argument('--subject', dest='subject_short_name', help='filter subject')
        parser.add_argument('--semester', dest='period_short_name', help='filter semester')
        parser.add_argument('--assignment-name', dest='assignment_short_name', help='filter name of assignment')
        parser.add_argument('--assignment-id', dest='assignment_id', help='id of assignment')
        parser.add_argument('--id', dest='id', help='id of assignment group')
        parser.add_argument('--format', dest='format', choices=['json', 'pretty'], default='pretty')
        parser.set_defaults(func=AssignmentGroup.run)

    @classmethod
    def run(cls, args):
        try:
            kwargs = dict(
                search=args.search,
                ordering=args.ordering,
                subject_short_name=args.subject_short_name,
                period_short_name=args.period_short_name,
                assignment_short_name=args.assignment_short_name,
                assignment_id=args.assignment_id,
                id=args.id
            )
            api = AssignmentGroupApi(args.key, role=args.role, action=args.action, **kwargs)
        except HTTPError as e:
            print(colorize.colored_text(e, colorize.COLOR_RED))
            raise SystemExit()
        if args.format == 'json':
            print(api.get_json())
        else:
            api.pretty_print()
