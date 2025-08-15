"""
Author: Louis Goodnews
Date: 2025-08-15
"""

from pathlib import Path
from typing import Any, Dict, Final, List, Optional

from utils.dispatcher import dispatch
from utils.files import (
    create_directory_if_not_exists,
    create_symlink,
    file_exists,
    file_remove,
    iterate_files,
    remove_symlink,
    unpack_archive,
)
from utils.logging import debug, exception, info, warn

__all__: Final[List[str]] = [
    "install_mod",
    "uninstall_mod",
]


def install_mod(mod: Dict[str, Any]) -> bool:
    """
    Installs a mod.

    :param mod: The mod to install.
    :type mod: Dict[str, Any]

    :return: True if the mod was installed successfully, False otherwise.
    :rtype: bool
    """

    # Attempt to get the game
    game: Optional[Dict[str, Any]] = dispatch(
        event="REQUEST_GET_GAME_BY_ID",
        game_id=mod.get("game_id"),
        namespace="global",
    ).get("_on_request_get_game_by_id", None)

    # Check if the game is None
    if not game:
        # Log a warning message
        warn(
            message=f"Game with ID '{mod.get('game_id')}' not found",
            name="mod_installer.install_mod",
        )

        # Return False if the game was not found
        return False

    if not file_exists(path=Path(mod["mod_archive_location"])):
        # Log a warning message
        warn(
            message=f"Mod archive at '{mod.get('mod_archive_location')}' not found",
            name="mod_installer.install_mod",
        )

        # Return False if the mod archive was not found
        return False

    # Attempt to install the mod
    try:
        # Unpack the mod archive
        unpack_archive(
            destination=Path(mod["mod_install_location"]),
            source=Path(mod["mod_archive_location"]),
        )

        # Create a dictionary to store the symlinks
        symlinks: Dict[str, str] = {}

        # Iterate over the files in the mod install location
        for file_path in iterate_files(directory=Path(mod["mod_install_location"])):
            # Get the target path
            target_path: Path = Path(mod["symlink_target"]) / file_path.relative_to(
                Path(mod["mod_install_location"])
            )

            # Check if the parent directory exists
            if file_path.parent.is_dir():
                # Create the parent directory if it does not exist
                create_directory_if_not_exists(path=target_path.parent)

            # Create the symlink
            create_symlink(
                source=file_path,
                target=target_path,
            )

            # Add the symlink to the symlinks dictionary
            symlinks[str(file_path)] = str(target_path)

        # Update the mod
        mod["symlinks"] = symlinks

        # Dispatch the update mod event
        dispatch(
            event="REQUEST_UPDATE_MOD",
            id=mod["id"],
            namespace="global",
            symlink_target=mod["symlink_target"],
            symlinks=symlinks,
        )
    except Exception as e:
        # Log an exception
        exception(
            exception=e,
            message="Caught an exception while attempting to install mod",
            name="mod_installer.install_mod",
        )

        # Broadcast the mod install failed event
        dispatch(
            event="BROADCAST_MOD_INSTALL_FAILED",
            game=game,
            mod=mod,
            namespace="global",
        )

        # Return False if the mod was not installed successfully
        return False

    # Broadcast the mod installed event
    dispatch(
        event="BROADCAST_MOD_INSTALL_SUCCESS",
        game=game,
        mod=mod,
        namespace="global",
    )

    # Log an info message
    info(
        message=f"Installed mod at '{mod.get('mod_install_location')}'",
        name="mod_installer.install_mod",
    )

    # Return True if the mod was installed successfully
    return True


def uninstall_mod(mod: Dict[str, Any]) -> bool:
    """
    Uninstalls a mod.

    :param mod: The mod to uninstall.
    :type mod: Dict[str, Any]

    :return: True if the mod was uninstalled successfully, False otherwise.
    :rtype: bool
    """

    # Attempt to get the game
    game: Optional[Dict[str, Any]] = dispatch(
        event="REQUEST_GET_GAME_BY_ID",
        game_id=mod.get("game_id"),
        namespace="global",
    ).get("_on_request_get_game_by_id", None)

    # Check if the game is None
    if not game:
        # Log a warning message
        warn(
            message=f"Game with ID '{mod.get('game_id')}' not found",
            name="mod_installer.uninstall_mod",
        )

        # Return False if the game was not found
        return False

    if not file_exists(path=Path(mod["mod_install_location"])):
        # Log a warning message
        warn(
            message=f"Mod install location at '{mod.get('mod_install_location')}' not found",
            name="mod_installer.uninstall_mod",
        )

        # Return False if the mod install location was not found
        return False

    # Attempt to uninstall the mod
    try:
        # Remove the symlink
        remove_symlink(path=Path(mod["mod_install_location"]))

        # Remove the mod install location
        file_remove(path=Path(mod["mod_install_location"]))
    except Exception as e:
        # Log an exception
        exception(
            exception=e,
            message="Caught an exception while attempting to uninstall mod",
            name="mod_installer.uninstall_mod",
        )

        # Return False if the mod was not uninstalled successfully
        return False

    # Broadcast the mod uninstalled event
    dispatch(
        event="BROADCAST_MOD_UNINSTALLED",
        game=game,
        mod=mod,
        namespace="global",
    )

    # Log an info message
    info(
        message=f"Uninstalled mod at '{mod.get('mod_install_location')}'",
        name="mod_installer.uninstall_mod",
    )

    # Return True if the mod was uninstalled successfully
    return True


def update_mod(mod: Dict[str, Any]) -> bool:
    """
    Updates a mod.

    :param mod: The mod to update.
    :type mod: Dict[str, Any]

    :return: True if the mod was updated successfully, False otherwise.
    :rtype: bool
    """

    # Attempt to uninstall the mod
    if not uninstall_mod(mod=mod):
        # Return False if the mod was not uninstalled successfully
        return False

    # Attempt to install the mod
    if not install_mod(mod=mod):
        # Return False if the mod was not installed successfully
        return False

    # Log an info message
    info(
        message=f"Updated mod at '{mod.get('mod_install_location')}'",
        name="mod_installer.update_mod",
    )

    # Return True if the mod was updated successfully
    return True
