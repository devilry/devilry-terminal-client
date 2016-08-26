from devilry.utils.basescript import BaseScript
from devilry.devilry_api.groupComment import GroupComment as Gcomment
from requests.exceptions import HTTPError
from devilry.utils import colorize
from devilry.utils import cliutils


class GroupComment(BaseScript):

    command = 'group-comment'
    parser = None

    @classmethod
    def add_to_subparser(cls, subparser):
        cls.parser = subparser.add_parser(cls.command, help='Devilry group comment.')
        cls.parser.add_argument('-k', '--key', dest='key', help='Api key', required=True)
        cls.parser.add_argument('-r', '--role', dest='role', choices=['student', 'examiner'], required=True)
        cls.parser.add_argument('--list', dest='action', action='store_const', const='list')
        cls.parser.add_argument('--new', dest='action', action='store_const', const='new')
        cls.parser.add_argument('--ordering-asc', dest='ordering_asc',
                                choices=['id', 'published_datetime', 'part_of_grading'],
                                default=None, help='Ascending order.')
        cls.parser.add_argument('--ordering-desc', dest='ordering_desc',
                                choices=['id', 'published_datetime', 'part_of_grading'],
                                default=None, help='Descending order.')
        cls.parser.add_argument('--feedback-set', dest='feedback_set', help='Id of feedbackset', required=True)
        cls.parser.add_argument('--id', dest='id', help='Id of comment.')
        cls.parser.add_argument('--text', dest='text', help='Comment text to post')
        cls.parser.add_argument('--format', dest='format', choices=['json', 'pretty'],
                                default='pretty', help='Output format.')
        cls.parser.set_defaults(func=GroupComment.run)

    @classmethod
    def run(cls, args):
        if args.action == 'new' and not args.text:
            cls.parser.error('--text is required when --new')

        ordering = args.ordering_asc or args.ordering_desc or None
        if args.ordering_desc:
            ordering = '-{}'.format(ordering)
        try:
            kwargs = dict(ordering=ordering, id=args.id)
            api = Gcomment(args.key, args.role, args.feedback_set, action=args.action,
                           text=args.text or None, **kwargs)

        except HTTPError as e:
            cliutils.print_error(e)
            raise SystemExit()
        if args.format == 'json':
            print(api.get_json())
        else:
            api.pretty_print()
