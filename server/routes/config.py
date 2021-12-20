from fastapi import APIRouter

router = APIRouter()
prefix = "/config-base"

BASE_CONFIG: str = """{
	"input_sep": ">>",
	"flag_prefix": "--",
	"colorize": true,
	"check_latest": true,
	"use_path_env": true,
	"hide_exe_from_help": true,
	"aliases": {
		"echo": "print",
		"ls": "listdir",
		"md": "create dir",
		"mk": "create file",
		"set": "var",
		"cd": "path",
		"rm": "remove dir",
		"rd": "remove file",
		"delete": "remove",
		"cls": "clear",
		"touch": "create file",
		"config": "json '{config}'",
		"end": "exit"
	},
	"comments": ["//", "#"],
	"functions": ["{", "}"],
	"help_command": "help",
	"seperator": ";",
	"errors": {
		"unknown_command": "Unknown command. Use {normal}{green}\\"help\\"{bright_red} to see commands.",
		"command_error": "{bright_red}Exception occured when running command {bright_green}\\"{cmd}\\"{bright_red}.{reset}",
		"function_open": "Function is already open.",
		"function_not_open": "Function is not open.",
		"function_undefined": "No function currently defined.",
		"permission_error": "Control Manual does not have permission to do this."
	},
	"cm_dir": "/mnt/e/Projects/Python/Control Manual/app"
}"""


@router.get("/")
def config_base() -> dict:
    return {"base": BASE_CONFIG, "status": 200}
