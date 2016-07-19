# devilry-terminal-client
Terminal API and client for handling terminal management and customized tasks. Closely integrated with specialized api in the main code-base

How to create plugins
===================
Plugins will be installed in the plugins folder, and your plugin.py file must be named as the plugin command.

Example:
```{r, engine='bash', count_lines}
$ tree
├── plugins
│   ├── myplugin.py
│   └── __init__.py
$ devil
usage: devil <command> <args>
$ devil myplugin -h
```

Example myplugin.py with argparse:
```python
class MyPlugin(BasePlugin):

	def __init__():
		self.parser = argparse.ArgumentParser(description=self.description(),
												prog='devil myplugin')
		self.parser.add_argument('-a', '--action', dest='action' help='something')

	@classmethod
	def description(cls):
		return 'plugin description'

	def run(self, args):
		args = self.parser.parse_arguments(args)
		...

#: register our plugin class
plugin = MyPlugin
```