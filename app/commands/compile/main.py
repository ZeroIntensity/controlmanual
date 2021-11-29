from typing import List, Dict
from src import Client # Only used for intellisense, will not work if this file is run manually.
import os

HELP: str = 'Run a Control Manual script.'
USAGE: str = '<file>'
ARGS: dict = {'file': 'File to run.'}
ARGS_HELP: dict = {
    'file': {
        'type': 'Path'
    }
}
PACKAGE: str = 'builtin'

def run(raw: str, args: List[str], kwargs: Dict[str, str], flags: List[str], client: Client):

    utils = client.utils
    errors = client.errors

    if not args:
        raise errors.NotEnoughArguments('Please specify a file.')

    path: str = utils.get_path(client.path, args[0], file = True)
    
    if not path:
        raise errors.NotExists(f'File "{args[0]}" was not found.')
    
    with open(path) as f:
        read: str = f.read()

    for i in read.split('\n'):
        client.run_command(i)
    
    return utils.make_meta()
    

