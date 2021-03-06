from devilry import settings
from devilry.utils.basescript import BaseScript
from devilry.devilry_api import FeedbacksetList
from devilry.api_client import Client
from requests.exceptions import HTTPError
from devilry.utils import colorize


class Feedbackset(BaseScript):

    command = 'feedbackset'

    @classmethod
    def add_to_subparser(cls, subparser):
        parser = subparser.add_parser(cls.command, help='Devilry api feedback set')
        parser.add_argument('-k', '--key', dest='key', help='Api key.', required=True)
        parser.add_argument('-r', '--role', dest='role', choices=['student', 'examiner'], required=True)
        parser.add_argument('--new', dest='action', action='store_const', const='new', help='Create new feedback set.')
        parser.add_argument('--ordering-asc', dest='ordering_asc',
                            choices=['id', 'deadline_datetime', 'created_datetime'],
                            default=None, help='Ascending order.')
        parser.add_argument('--ordering-desc', dest='ordering_desc',
                            choices=['id', 'deadline_datetime', 'created_datetime'],
                            default=None, help='Descending order.')
        parser.add_argument('--group-id', dest='group_id', help='Group id of feedbackset.')
        parser.add_argument('--id', dest='id', help='id of feedbackset')
        parser.add_argument('--format', dest='format', choices=['json', 'pretty'],
                            default='pretty', help='Output format.')
        parser.set_defaults(func=Feedbackset.run)

    @classmethod
    def run(cls, args):
        ordering = args.ordering_asc or args.ordering_desc or None
        if args.ordering_desc:
            ordering = '-{}'.format(ordering)
        try:
            kwargs = dict(
                ordering=ordering,
                group_id=args.group_id,
                id=args.id
            )
            client = Client(settings.API_URL)
            client.auth(key=args.key)
            api = FeedbacksetList(client, args.role, **kwargs)
            api.feedbackset_list
        except HTTPError as e:
            print(colorize.colored_text(e, colorize.COLOR_RED))
            raise SystemExit()
        api.pretty_print()
