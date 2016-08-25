import sys
from . import colorize


def utf8print(unicodestring):
    print(unicodestring.encode(sys.stdout.encoding, "replace"))


def print_error(errormessage, prefix=u'ERROR: '):
    utf8print(colorize.colored_text(
        u'{}{}'.format(prefix, errormessage),
        color=colorize.COLOR_RED, bold=True))


def print_warning(warningmessage, prefix=u'WARNING: '):
    utf8print(colorize.colored_text(
        u'{}{}'.format(prefix, warningmessage),
        color=colorize.COLOR_YELLOW, bold=True))


def print_success(successmessage):
    utf8print(colorize.colored_text(
        successmessage,
        color=colorize.COLOR_GREEN))
