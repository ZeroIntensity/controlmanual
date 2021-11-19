import os

BASE: str = """from typing import List, Dict
from src import Client # Only used for intellisense, will not work if this file is run manually.

HELP: str = 'Basic command.'
USAGE: str = '<message>'
ARGS: dict = {'message': 'Message to print.'}
FLAGS: dict = {'hello_world': 'Whether to print "Hello World".'}
PACKAGE: str = '{pkg_name}'

def run(raw: str, args: List[str], kwargs: Dict[str, str], flags: List[str], client: Client):

    config = client.config
    utils = client.utils
    api = client.api
    static = client.static

    if not args:
        return utils.error('Please specify a message.')

    if 'hello_world' in flags:
        print("Hello World")
    else:
        print(args[0])
"""

MIDDLEWARE: str = '''from typing import List, Dict
from src import Client # Only used for intellisense, will not work if this file is run manually.

def run(command: str, raw: str, args: List[str], kwargs: Dict[str, str], flags: List[str], client: Client):
    print(f'Command "{command}" was run!')
'''

from typing import List, Dict
from src import Client # Only used for intellisense, will not work if this file is run manually.

HELP: str = 'Initalize a command or middleware.'
USAGE: str = '<name> [flags]'
ARGS: dict = {'name': 'Name of the command.'}
FLAGS: dict = {'here': 'Initalizes the command in the current directory.', 'middleware': 'Initalizes middleware instead of a command.'}
PACKAGE: str = 'builtin'

def run(raw: str, args: List[str], kwargs: Dict[str, str], flags: List[str], client: Client):
    utils = client.utils
    config = client.config

    typ: str = 'command' if 'middleware' not in flags else 'middleware'

    if len(args) == 0:
        return utils.error(f'Please specify a {typ} name.')

    directory: str = os.path.join(
        os.path.join(
            config.cm_dir,
            'commands' if typ == 'command' else 'middleware'
        ),
        args[0]
    ) if 'here' not in flags else os.path.join(client.path, args[0])

    if os.path.exists(directory):
        return utils.error(f'{typ.capitalize()} already exists.{utils.reset}')

    os.makedirs(directory)

    with open(os.path.join(directory, 'main.py'), 'w') as f:
        f.write(BASE.replace('{pkg_name}', args[0]) if 'middleware' not in flags else MIDDLEWARE)

    client.reload()
    utils.success(f'Successfully initalized {typ} "{args[0]}".')