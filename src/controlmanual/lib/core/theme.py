from rich.console import Console
from rich.theme import Theme

from .config import config

tc = config["truecolor"]

red = config["colors"]["red"]
green = config["colors"]["green"]
dark_green = config["colors"]["dark_green"]

primary: str = f"{green}" if tc else "green"

theme = Theme(
    {
        "error": f"bold {red}" if tc else "bold red",
        "important": f"bold {green}" if tc else "bold green",
        "success": primary,
        "primary": primary,
        "secondary": f"{dark_green}" if tc else "dim green",
    }
)
console_object = Console(theme=theme, color_system="truecolor" if tc else "standard")
