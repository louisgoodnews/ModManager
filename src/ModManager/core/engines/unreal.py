"""
Author: Louis Goodnews
Date: 2025-08-12
"""

from pathlib import Path
from typing import Any, Final, List, Set, Union

from utils.files import create_directory, directory_exists, list_directory_contents
from utils.logging import warn


__all__: Final[List[str]] = ["create_mods_folder", "is_unreal_game"]


def create_mods_folder(path: Union[str, Path]) -> None:
    """
    Creates a mods folder at the specified path.

    :param path: The path to the mods folder.
    :type path: Union[str, Path]

    :return: None
    :rtype: None
    """

    # Check if the path is a Path object
    if not isinstance(
        path,
        Path,
    ):
        # Convert the path to a Path object
        path = Path(path)

    # Create the mods folder
    create_directory(path=path.joinpath("Content/Paks/~mods"))


def is_unreal_game(path: Union[str, Path]) -> bool:
    """
    Checks if the given path is a valid Unreal game directory.

    :param path: The path to check.
    :type path: Union[str, Path]

    :return: True if the path is a valid Unreal game directory, False otherwise.
    :rtype: bool
    """

    # Check if the path is a Path object
    if not isinstance(
        path,
        Path,
    ):
        # Convert the path to a Path object
        path = Path(path)

    # Check if the directory exists
    if not directory_exists(path=path):
        # Log a warning
        warn(
            message=f"Directory '{path}' does not exist",
            name="unreal.is_unreal_game",
        )

        # Return False
        return False

    # List the directory contents
    # Top-level directories present?
    contents: List[Dict[str, Any]] = list_directory_contents(path=path)
    top_dirs: Set[str] = {item["name"] for item in contents if item["is_dir"]}

    required_top_dirs: Set[str] = {
        "Engine",
        "Content",
        "Binaries",
    }

    if not required_top_dirs.issubset(top_dirs):
        return False

    # Check inside Engine
    engine_path: Path = Path(
        path,
        "Engine",
    )

    engine_contents: Set[str] = {
        item["name"] for item in list_directory_contents(engine_path) if item["is_dir"]
    }

    if not {
        "Binaries",
        "Config",
        "Content",
        "Plugins",
    }.issubset(engine_contents):
        return False

    # Check Content/Paks
    if not directory_exists(
        path=Path(
            engine_path.parent,
            "Content",
            "Paks",
        )
    ):
        return False

    # Check for platform folder in Binaries (e.g., Win64/Win32)
    binaries_contents: Set[str] = {
        item["name"]
        for item in list_directory_contents(
            path=Path(
                engine_path.parent,
                "Binaries",
            )
        )
        if item["is_dir"]
    }

    if not {
        "Win64",
        "Win32",
    }.issubset(binaries_contents):
        return False

    return True
