from devilry.utils.basescript import BaseScript
from devilry.devilry_api import AssignmentList
from devilry.api_client import Client
from devilry import settings
from requests.exceptions import HTTPError
from devilry.utils import cliutils


class Assignment(BaseScript):

    command = 'assignment'

    @classmethod
    def add_to_subparser(cls, subparser):
        parser = subparser.add_parser(cls.command, help='Devilry api assignment.')
        parser.add_argument('-k', '--key', dest='key', help='Api key.', required=True)
        parser.add_argument('-r', '--role', dest='role', choices=['student', 'examiner'], required=True)
        parser.add_argument('--ordering-asc', dest='ordering_asc',
                            choices=['publishing_date', 'publishing_time', 'short_name'],
                            default=None, help='Ascending order.')
        parser.add_argument('--ordering-desc', dest='ordering_desc',
                            choices=['publishing_date', 'publishing_time', 'short_name'],
                            default=None, help='Descending order.')
        parser.add_argument('--search', dest='search', help='Search field(semester, subject, assignment name).')
        parser.add_argument('--subject', dest='subject_short_name', help='Filter subject.')
        parser.add_argument('--semester', dest='period_short_name', help='Filter semester.')
        parser.add_argument('--assignment-name', dest='short_name', help='Filter name of assignment.')
        parser.add_argument('--id', dest='id', help='Id of assignment.')
        parser.add_argument('--format', dest='format', choices=['json', 'pretty'],
                            default='pretty', help='Output format.')
        parser.set_defaults(func=Assignment.run)

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
                short_name=args.short_name,
                id=args.id
            )
            client = Client(settings.API_URL)
            client.auth(key=args.key)
            api = AssignmentList(client, args.role, **kwargs)
            api.assignment_list
        except HTTPError as e:
            cliutils.print_error(e)
            raise SystemExit()
        api.pretty_print()
