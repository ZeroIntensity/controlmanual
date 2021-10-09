from typing import List, Dict
from src import Client # Only used for intellisense, will not work if this file is run manually.

HELP: str = 'Reload all commands and middleware.'
USAGE: str = '[flags]'
ARGS: dict = {}
FLAGS: dict = {'hard': 'Entirely reload the Control Manual instance.'}

def run(raw: str, args: List[str], kwargs: Dict[str, str], flags: List[str], client: Client):
    if 'hard' in flags:
        return client.invoke_reset()

    client.reload()

    return client.utils.success('Reloaded commands and middleware.')