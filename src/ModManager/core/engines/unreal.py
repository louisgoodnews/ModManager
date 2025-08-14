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
            message=f"Directory '{path}' does not exist. Aborting.",
            name="unreal.is_unreal_game",
        )

        # Return False
        return False

    # Check for a .uproject file
    for item in list_directory_contents(path=path):
        # Check if the item is a .uproject file
        if not item["name"].endswith(".uproject"):
            # Skip the current iteration
            continue

        # Return True
        return True

    # Check for win64 binaries
    binaries_path_64: Path = path.joinpath(
        "Binaries",
        "Win64",
    )

    # Check for win32 binaries
    binaries_path_32: Path = path.joinpath(
        "Binaries",
        "Win32",
    )

    # Check if the win64 binaries exist
    if directory_exists(path=binaries_path_64):
        # Set the binaries path
        binaries_path: Path = binaries_path_64

        # Set the suffix
        suffix: str = "-Win64-Shipping.exe"
    # Check if the win32 binaries exist
    elif directory_exists(path=binaries_path_32):
        # Set the binaries path
        binaries_path: Path = binaries_path_32

        # Set the suffix
        suffix: str = "-Win32-Shipping.exe"
    else:
        # Return False if neither win64 nor win32 binaries exist
        warn(
            message=f"Directory '{path}' does not contain win64 or win32 binaries. Aborting.",
            name="unreal.is_unreal_game",
        )

        # Return False
        return False

    # Check for a Shipping.exe file
    for item in list_directory_contents(path=binaries_path):
        # Check if the item is a Shipping.exe file
        if not item["name"].endswith(suffix):
            # Skip the current iteration
            continue

        # Return True
        return True

    # Return False
    return False
