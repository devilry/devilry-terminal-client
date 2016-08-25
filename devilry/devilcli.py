import argparse
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from devilry.external_plugins.config import INSTALLED_PLUGINS


def main():
    parser = argparse.ArgumentParser(prog='devil')
    subparsers = parser.add_subparsers(help='Commands')

    for plugin in INSTALLED_PLUGINS:
        plugin.add_to_subparser(subparsers)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_usage()

if __name__ == '__main__':
    main()
