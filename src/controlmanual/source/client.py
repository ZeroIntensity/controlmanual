import logging
import os
import shutil
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type

import colorama
import dload
import toml
from rich.console import Console
from typeguard import typechecked

from .constants import cm_dir, errors
from .constants.errors import (
    InvalidArguments,
    Other,
    NotEnoughArguments,
    Exists,
    NotExists,
    InvalidArgument,
    APIError,
    NothingChanged,
    Collision,
)
from .core.config import config as conf
from .core.handler import CommandHandler
from .core.loader import load_commands
from .typings import CommandCallable, CommandIterator, Config
from .utils import commands
from .utils import title as titl

if TYPE_CHECKING:
    from .app import Application

__all__ = ["Client"]


class Client:
    """Class for allowing commands to interact with the engine."""

    async def init(self, app: "Application") -> None:
        self._reset: bool = False
        self._path: Path = Path().home()
        self._functions: dict = {}
        self._current_function: Optional[str] = None
        self._function_open: bool = False
        self._toggled_output: bool = True
        self._origin: Path = self._path
        self._command_response: Any = None
        self._app = app

        def get(x):
            return os.path.join(cm_dir, x)

        self._variables: Dict[str, str] = {
            "path": str(self._path),
            "config": self.config_path,
            "cmdir": cm_dir,
            "logs": get("logs"),
            "commands": get("commands"),
            "middleware": get("middleware"),
        }
        self._aliases: Dict[str, str] = {}
        self._vals: Dict[Any, Any] = {}

        for i in conf["aliases"]:
            self._aliases[i] = await self.load_variables(conf["aliases"][i])

        colorama.init(convert=os.name == "nt")  # enables ansi stuff

        titl("Control Manual")
        self._history: List[str] = []

        self.install()
        await self.render()

    def install(self):
        with open(os.path.join(cm_dir, "config-lock.toml")) as f:
            lock = toml.load(f)

        if not lock["environment"]["installed"]:
            with Console().status("Installing...", spinner="material"):
                try:
                    target: str = os.path.join(cm_dir, "commands")
                    dload.git_clone(
                        "https://github.com/ControlManual/ControlManual-builtin.git",
                        target,
                    )
                    source: str = os.path.join(target, "ControlManual-Builtin-master")

                    file_names = os.listdir(source)

                    for file_name in file_names:
                        shutil.move(os.path.join(source, file_name), target)

                    os.rmdir(source)
                    lock["environment"]["installed"] = True
                except Exception as e:
                    logging.error(f"failed to install builtins: {e}")
                    self.error(
                        "Could not install builtins. Check the logs for more info."
                    )

        with open(os.path.join(cm_dir, "config-lock.toml"), "w") as f:
            toml.dump(lock, f)

    @staticmethod
    def title(t: str) -> None:
        """Set the terminal title."""
        titl(t)

    async def render(self) -> None:
        """Function for loading commands."""
        self._commands = await load_commands()

    @property
    def app(self) -> "Application":
        """Textual app class."""
        return self._app

    @property
    def cm_dir(self) -> str:
        """Top level directory of Control Manual."""
        return cm_dir

    @property
    def config_path(self) -> str:
        """Location of the config file."""
        return os.path.join(cm_dir, "config.json")

    @property
    def cmd_history(self) -> List[str]:
        """Get the command history."""
        return self._history

    @property
    def function_open(self) -> bool:
        """Whether a function is currently being edited."""
        return self._function_open

    @function_open.setter
    def function_open(self, value: bool) -> None:
        self._function_open = value

    @property
    def functions(self) -> dict:
        """Dictionary of defined functions."""
        return self._functions

    @property
    def current_function(self) -> Optional[str]:
        """Current function being edited."""
        return self._current_function

    @current_function.setter
    def current_function(self, value: str) -> None:
        self._current_function = value

    @property
    def vals(self) -> Dict[Any, Any]:
        """Namespace for commands and middleware to hold values."""
        return self._vals

    @vals.setter
    def vals(self, key: Any, value: Any) -> None:
        self._vals[key] = value

    @property
    def config(self) -> Config:
        """Class for representing the JSON config."""
        return conf

    @property
    def origin(self) -> Path:
        """Original path from initalization."""
        return self._origin

    @property
    def aliases(self) -> Dict[str, str]:
        """Command aliases."""
        return self._aliases

    async def add_alias(self, alias: str, value: str) -> None:
        """Function for adding command aliases."""
        self._aliases[alias] = await self.load_variables(value)

    @property
    def version(self) -> str:
        """Version of Control Manual."""
        raise NotImplementedError("version tracking not yet implemented")

    @property
    def commands(self):
        """Dictionary representation of commands."""
        return self._commands

    @property
    def path(self) -> Path:
        """Current path object."""
        return self._path

    @property
    def path_str(self) -> str:
        """Current path object as a string."""
        return str(self._path)

    @property
    def variables(self) -> Dict[str, str]:
        """Dictionary representing variables."""
        return self._variables

    def add_variable(self, name: str, value: str) -> None:
        """Function for adding a variable to the instance."""
        self._variables[name] = value

    def change_path(self, path: Path) -> None:
        """Function for changing the current path."""
        self._path = path

    def invoke_reset(self) -> None:
        """Tell the Control Manual instance to reset after the current command has finished. Only works when run via the main file."""
        self._reset = True

    async def load_variables(self, text: str) -> str:  # type: ignore
        """Function for loading variables into a string."""

        for key, value in self.variables.items():
            text = text.replace("{" + key + "}", value)

        return text

    async def _format_string(self, collection: dict, text: str) -> str:
        for key, value in collection.items():
            text = text.replace("{" + key + "}", value)

        return text

    @property
    def error_map(self) -> List[Type[Exception]]:
        """Map of errors and their corresponding metadata."""
        return [
            InvalidArguments,
            Other,
            NotEnoughArguments,
            Exists,
            NotExists,
            InvalidArgument,
            APIError,
            NothingChanged,
            Collision,
        ]

    async def run_command(self, command: str):
        """Run a command."""
        await CommandHandler(self).run_string(command)

    @staticmethod
    @typechecked
    def command(func: CommandCallable):
        """Decorator for making sure a command is valid."""
        return func

    @staticmethod
    @typechecked
    def iterator(func: CommandIterator):
        """Decorator for making sure an iterator command is valid."""
        return func

    @property
    def utils(self):
        """Utilities for commands to use."""
        return commands

    @property
    def errors(self):
        return errors

    @property
    def console(self):
        return self._app.interface.console_client

    def print(self, *args: Any) -> None:
        """Print a message to the terminal"""
        self.console.print(*args)

    def error(self, *args: Any) -> None:
        """Print an error message to the terminal."""
        self.console.error(*args)

    def success(self, *args: Any) -> None:
        """Print a success message to the terminal."""
        self.console.success(*args)

    async def show_exc(self, exc: Exception) -> None:
        """Display the exception on the ExcPanel widget."""
        await self._app.show_exc(exc)