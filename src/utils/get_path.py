import os
from typing import Union

def get_path(current_path: str, path: str, file: bool = False) -> Union[None, str]:
    """Function for checking if a path exists globally, or in the current directory. Returns None if not found."""
    merged: str = os.path.join(current_path, path)
    if not os.path.exists(merged):
        if not os.path.exists(path):
            return None
        else:
            if os.path.isfile(path):
                return path if file else None
    else:
        if os.path.isfile(path):
            return merged if file else None