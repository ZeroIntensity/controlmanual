from typing import List, Dict
from src import Client # Only used for intellisense, will not work if this file is run manually.

HELP: str = 'Call a function.'
USAGE: str = '<function> [arguments]'
ARGS: dict = {'functions': 'Name of the function.', 'arguments': 'Arguments to pass into the function.'}
FLAGS: dict = {}
PACKAGE: str = 'builtin'

def run(raw: str, args: List[str], kwargs: Dict[str, str], flags: List[str], client: Client):

    utils = client.utils

    if args == []:
        return utils.error('Please specify a function name.')

    fn = client.functions.get(args[0])

    if not fn:
        return utils.error('Please specify a valid function.')

    arguments = fn['arguments']
    params = args[1:]

    if not fn['defined']:
        return utils.error(f'Function "{args[0]}" is defined, but does not have a body.')

    if not len(arguments) == len(params):
        return utils.error('Missing function parameters.')

    for i in fn['script']:
        text = i
        variables: dict = {}

        for index, value in enumerate(arguments):
            variables[value] = params[index]

        text = client.load_variables_dynamic(text, variables)
        client.run_command(text)