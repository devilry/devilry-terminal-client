#!/usr/bin/env python

import argparse
from devilry.external_scripts.config import INSTALLED_SCRIPTS


def main():
    parser = argparse.ArgumentParser(prog='devil')
    subparsers = parser.add_subparsers(help='Commands')

    for plugin in INSTALLED_SCRIPTS:
        plugin.add_to_subparser(subparsers)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_usage()

if __name__ == '__main__':
    main()
