# devilry-terminal-client
Terminal API and client for handling terminal management and customized tasks. Closely integrated with specialized api in the main code-base

How to create scripts
====================
Become a real devil and create your own scritps!

Example cli.py:
```python
from devilry.utils.basescript import BaseScript
class MyScript(BaseScript):

    command = 'my-script'

    @classmethod
    def add_to_supparser(cls, subparser):
        parser = subparser.add_parser(cls.command, help='my super cool script')
        parser.add_argument('--my-cool-argument', dest='my_arg', require=True)
        parser.set_defaults(func=MyScript.run)

    @classmethod
    def run(cls, args):
        ...

```

### External scripts
Install yor script here here:
```{r, engine='bash', count_lines}
$ tree
├── devilry
│   ├── external_scripts
|   |   ├── myscript
|   |   |   ├── cli.py
|   |   ├── ...
│   |   ├── config.py
|   ├── ...
├── ...
```
Register your script to config.py
```python
..
from devilry.external_scripts.cli import MyScript
INSTALLED_SCRIPTS = [
    ...
    MyScript,
]
```

### Local scripts
This is not supported yet, but here is the idea.

1. Create a directory for your local scripts in your home directory:
    ```{r, engine='bash', count_lines}
    $ mkdir /home/$USER/devilry_scripts
    ```

2. Export your local script folder path to your environment:
    ```{r, engine='bash', count_lines}
    $ export DEVILRY_LOCAL_SCRIPTS = /home/$USER/devilry_scripts
    ```

3. Create your config.py file:
    ```python
    ...
    from myscrip.cli import MyScript
    INSTALLED_SCRIPTS = [
        ...
        MyScript,
    ]
    ```

4. Your script folder should look like this:
    ```{r, engine='bash', count_lines}
    $ pwd
    /home/user/devilry_scripts
    $ tree
    ├── myscript
    |   ├── cli.py
    |   ...
    └── config.py
    ```
