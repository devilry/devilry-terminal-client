from devilry.utils.basescript import BaseScript
from devilry.devilry_api.groupComment import GroupComment as Gcomment
from requests.exceptions import HTTPError
from devilry.utils import colorize


class GroupComment(BaseScript):

    command = 'group-comment'

    @classmethod
    def add_to_subparser(cls, subparser):
        parser = subparser.add_parser(cls.command, help='devilry group comment')
        parser.add_argument('-k', '--key', dest='key', help='Api key', required=True)
        parser.add_argument('-r', '--role', dest='role', choices=['student', 'examiner'], required=True)
        parser.add_argument('-a', '--action', dest='action', choices=['list', 'new'])
        parser.add_argument('-o', '--ordering', dest='ordering',
                            choices=['id', 'published_datetime', 'part_of_grading',
                                     '-id', '-published_datetime', '-part_of_grading'],
                            default=None)
        parser.add_argument('--feedback-set', dest='feedback_set', help='feedbackset', required=True)
        parser.add_argument('--id', dest='id', help='id of comment')
        parser.add_argument('--format', dest='format', choices=['json', 'pretty'], default='pretty')
        parser.set_defaults(func=GroupComment.run)

    @classmethod
    def run(cls, args):
        try:
            kwargs = dict(ordering=args.ordering, id=args.id)
            api = Gcomment(args.key, args.feedback_set, role=args.role, action=args.action, **kwargs)

        except HTTPError as e:
            print(colorize.colored_text(e, colorize.COLOR_RED))
            raise SystemExit()
        if args.format == 'json':
            print(api.get_json())
        else:
            api.pretty_print()