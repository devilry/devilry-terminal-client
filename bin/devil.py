#!/usr/bin/env python
if __name__ == '__main__':
    import sys
    from devilryclientlib import utils

    try:
        command = sys.argv[1]
        args = sys.argv[2:]
        utils.execute(command, args)
    except IndexError:
        utils.showhelp()
        raise SystemExit()
