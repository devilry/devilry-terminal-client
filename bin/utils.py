import sys
from os.path import dirname, join, exists
from os import listdir
import importlib


def execute(command, args):
    """
    Execute command by calling the corresponding py-file with args as arguments
    """
    path = join(getpluginsdir(), command + ".py")
    if exists(path):
        print('wohoo')


def showhelp():
    """
    Print the help menu
    """
    commands = getcommandlist()
    print('Usage: {} <action> <args>'.format(sys.argv[0]))
    print('Actions:')
    for cmd in commands:
        plugin = 'plugins.{}'.format(cmd[:-3])
        try:
            description = getattr(importlib.import_module(plugin), 'description')()
        except AttributeError:
            description = 'No description'
        print('     {}: {}'.format(cmd[:-3], description))


def getcommandlist():
    """
    Return:
         All available commands
    """
    filenames = listdir(join(dirname(dirname(__file__)), 'plugins'))
    commands = [filename for filename in filenames if filename.endswith('.py') and not filename.startswith('__')]
    return commands


def getpluginsdir():
    """
    Returns:
        Plugins directory
    """
    parentdir = dirname(dirname(__file__))
    return join(parentdir, "plugins")