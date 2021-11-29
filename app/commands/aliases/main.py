from typing import List, Dict
from src import Client # Only used for intellisense, will not work if this file is run manually.

HELP: str = 'Get command aliases.'
PACKAGE: str = 'builtin'

def run(raw: str, args: List[str], kwargs: Dict[str, str], flags: List[str], client: Client):

    aliases: Dict[str, str] = client.aliases
    console = client.console
    errors = client.errors
    utils = client.utils

    if not aliases:
        raise errors.NothingChanged('No aliases exist.')

    for key, value in aliases.items():
        console.key_value(key, value)
    
    return utils.make_meta()