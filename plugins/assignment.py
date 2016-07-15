import argparse
from lib.auth import add_api_key_args


def description():
    return 'list/get assignment'


class Assignment(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser('Devilry - list assignments')
        add_api_key_args(self.parser)

    def run(self):
        self.parser.parse_args()


if __name__ == '__main__':
    Assignment.run()