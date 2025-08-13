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

    # Check for a .uproject file
    for item in list_directory_contents(path=path):
        if item["name"].endswith(".uproject"):
            return True

    # Check for binaries
    binaries_path_64 = path.joinpath("Binaries", "Win64")
    binaries_path_32 = path.joinpath("Binaries", "Win32")

    if directory_exists(path=binaries_path_64):
        binaries_path = binaries_path_64
        suffix = "-Win64-Shipping.exe"
    elif directory_exists(path=binaries_path_32):
        binaries_path = binaries_path_32
        suffix = "-Win32-Shipping.exe"
    else:
        return False

    # Check for a Shipping.exe file
    for item in list_directory_contents(path=binaries_path):
        if item["name"].endswith(suffix):
            return True

    return False
