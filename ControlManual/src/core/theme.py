from rich.theme import Theme
from rich.console import Console
from .config import config

tc = config['truecolor']

red = config['colors']['red']
green = config['colors']['green']

theme = Theme({
    "error": f"bold {red}" if tc else 'bold red',
    "important": f"bold {red}" if tc else 'bold green',
    "success": f"{green}" if tc else 'green'
})
console_object = Console(theme = theme, color_system = 'truecolor' if tc else 'standard')