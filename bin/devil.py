#!/usr/bin/env python
if __name__ == '__main__':
    import sys
    from bin import utils

    try:
        command = sys.argv[1]
        args = sys.argv[2:]
    except IndexError:
        utils.showhelp()
        raise SystemExit()
