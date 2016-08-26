from devilry.utils.basescript import BaseScript
from devilry.devilry_api.feedbackset import Feedbackset as Fset
from requests.exceptions import HTTPError
from devilry.utils import colorize


class Feedbackset(BaseScript):

    command = 'feedbackset'

    @classmethod
    def add_to_subparser(cls, subparser):
        parser = subparser.add_parser(cls.command, help='devilry feedback set')
        parser.add_argument('-k', '--key', dest='key', help='Api key', required=True)
        parser.add_argument('-r', '--role', dest='role', choices=['student', 'examiner'], required=True)
        parser.add_argument('-a', '--action', dest='action', choices=['list', 'new'])
        parser.add_argument('-o', '--ordering', dest='ordering',
                            choices=['id', 'deadline_datetime', 'created_datetime',
                                     '-id', '-deadline_datetime', '-created_datetime'],
                            default=None)
        parser.add_argument('--group-id', dest='group_id', help='group id of feedbackset')
        parser.add_argument('--id', dest='id', help='id of feedbackset')
        parser.add_argument('--format', dest='format', choices=['json', 'pretty'], default='pretty')
        parser.set_defaults(func=Feedbackset.run)

    @classmethod
    def run(cls, args):
        try:
            kwargs = dict(
                ordering=args.ordering,
                group_id=args.group_id,
                id=args.id
            )
            api = Fset(args.key, role=args.role, action=args.action, **kwargs)
        except HTTPError as e:
            print(colorize.colored_text(e, colorize.COLOR_RED))
            raise SystemExit()
        if args.format == 'json':
            print(api.get_json())
        else:
            api.pretty_print()
