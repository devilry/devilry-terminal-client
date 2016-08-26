from devilry.utils.basescript import BaseScript
from devilry.devilry_api.assignmentGroup import AssignmentGroup as AssignmentGroupApi
from requests.exceptions import HTTPError
from devilry.utils import cliutils


class AssignmentGroup(BaseScript):

    command = 'assignment-group'

    @classmethod
    def add_to_subparser(cls, subparser):
        parser = subparser.add_parser(cls.command, help='Devilry api assignment group.')
        parser.add_argument('-k', '--key', dest='key', help='Api key.', required=True)
        parser.add_argument('-r', '--role', dest='role', choices=['student', 'examiner'], required=True)
        parser.add_argument('--list', dest='action', action='store_const', const='list', help='List assignment groups.')
        parser.add_argument('--ordering-asc', dest='ordering_asc',
                            choices=['id', 'is_corrected', 'assignment_short_name'],
                            default=None, help='Ascending order.')
        parser.add_argument('--ordering-desc', dest='ordering_desc',
                            choices=['id', 'is_corrected', 'assignment_short_name'],
                            default=None, help='Descending order.')
        parser.add_argument('-s', '--search', dest='search', help='Search field(semester, subject, assignment name).')
        parser.add_argument('--subject', dest='subject_short_name', help='filter subject.')
        parser.add_argument('--semester', dest='period_short_name', help='filter semester.')
        parser.add_argument('--assignment-name', dest='assignment_short_name', help='Filter name of assignment.')
        parser.add_argument('--assignment-id', dest='assignment_id', help='Id of assignment.')
        parser.add_argument('--id', dest='id', help='Id of assignment group.')
        parser.add_argument('--format', dest='format', choices=['json', 'pretty'],
                            default='pretty', help='Output format.')
        parser.set_defaults(func=AssignmentGroup.run)

    @classmethod
    def run(cls, args):
        ordering = args.ordering_asc or args.ordering_desc or None
        if args.ordering_desc:
            ordering = '-{}'.format(ordering)
        try:
            kwargs = dict(
                search=args.search,
                ordering=ordering,
                subject_short_name=args.subject_short_name,
                period_short_name=args.period_short_name,
                assignment_short_name=args.assignment_short_name,
                assignment_id=args.assignment_id,
                id=args.id
            )
            api = AssignmentGroupApi(args.key, args.role, action=args.action, **kwargs)
        except HTTPError as e:
            cliutils.print_error(e)
            raise SystemExit()
        if args.format == 'json':
            print(api.get_json())
        else:
            api.pretty_print()
