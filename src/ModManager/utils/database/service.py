"""
Author: Louis Goodnews
Date: 2025-08-15
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Final, List, Optional, Union

from utils.database.games import (
    get_all_games,
    get_game_by_code,
    get_game_by_id,
    get_games_by_codes,
    get_games_by_ids,
    insert_game,
    search_games,
    update_game,
)
from utils.database.mods import (
    get_all_mods,
    get_mod_by_code,
    get_mod_by_id,
    get_mods_by_codes,
    get_mods_by_ids,
    get_mods_for_game,
    insert_mod,
    search_mods,
    update_mod,
)
from utils.dispatcher import register, unregister
from utils.logging import exception, info


__all__: Final[List[str]] = [
    "subscribe_to_events",
    "unsubscribe_from_events",
]


REGISTRATION_IDS: Final[List[str]] = []


def _on_broadcast_application_shutdown(event: Optional[str] = None) -> bool:
    """
    Unsubscribes from events.

    :param event: The event that triggered the function.
    :type event: Optional[str]

    :return: True if successful, False otherwise.
    :rtype: bool
    """

    # Log an info message
    info(
        message=f"Received '{event}' event. Unsubscribing from events...",
        name="database.service._on_broadcast_application_shutdown",
    )

    # Unsubscribe from events
    unsubscribe_from_events()

    # Return True
    return True


def _on_request_get_all_games(event: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Returns all games.

    :param event: The event that triggered the function.
    :type event: Optional[str]

    :return: The games.
    :rtype: List[Dict[str, Any]]
    """

    # Return the games
    return get_all_games()


def _on_request_get_all_mods(event: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Returns all mods.

    :param event: The event that triggered the function.
    :type event: Optional[str]

    :return: The mods.
    :rtype: List[Dict[str, Any]]
    """

    # Return the mods
    return get_all_mods()


def _on_request_get_game_by_code(
    game_code: str,
    event: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Returns a game by its code.

    :param game_code: The code of the game to retrieve.
    :type game_code: str
    :param event: The event that triggered the function.
    :type event: Optional[str]

    :return: The game.
    :rtype: Dict[str, Any]
    """

    # Return the game
    return get_game_by_code(game_code=game_code)


def _on_request_get_game_by_id(
    game_id: int,
    event: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Returns a game by its ID.

    :param game_id: The ID of the game to retrieve.
    :type game_id: int
    :param event: The event that triggered the function.
    :type event: Optional[str]

    :return: The game.
    :rtype: Dict[str, Any]
    """

    # Return the game
    return get_game_by_id(game_id=game_id)


def _on_request_get_games_by_codes(
    game_codes: List[str],
    event: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Returns games by their codes.

    :param game_codes: The codes of the games to retrieve.
    :type game_codes: List[str]
    :param event: The event that triggered the function.
    :type event: Optional[str]

    :return: The games.
    :rtype: List[Dict[str, Any]]
    """

    # Return the games
    return get_games_by_codes(game_codes=game_codes)


def _on_request_get_games_by_ids(
    game_ids: List[int],
    event: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Returns games by their IDs.

    :param game_ids: The IDs of the games to retrieve.
    :type game_ids: List[int]
    :param event: The event that triggered the function.
    :type event: Optional[str]

    :return: The games.
    :rtype: List[Dict[str, Any]]
    """

    # Return the games
    return get_games_by_ids(game_ids=game_ids)


def _on_request_get_mod_by_code(
    mod_code: str,
    event: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Returns a mod by its code.

    :param mod_code: The code of the mod to retrieve.
    :type mod_code: str
    :param event: The event that triggered the function.
    :type event: Optional[str]

    :return: The mod.
    :rtype: Dict[str, Any]
    """

    # Return the mod
    return get_mod_by_code(mod_code=mod_code)


def _on_request_get_mod_by_id(
    mod_id: int,
    event: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Returns a mod by its ID.

    :param mod_id: The ID of the mod to retrieve.
    :type mod_id: int
    :param event: The event that triggered the function.
    :type event: Optional[str]

    :return: The mod.
    :rtype: Dict[str, Any]
    """

    # Return the mod
    return get_mod_by_id(mod_id=mod_id)


def _on_request_get_mods_by_codes(
    mod_codes: List[str],
    event: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Returns mods by their codes.

    :param mod_codes: The codes of the mods to retrieve.
    :type mod_codes: List[str]
    :param event: The event that triggered the function.
    :type event: Optional[str]

    :return: The mods.
    :rtype: List[Dict[str, Any]]
    """

    # Return the mods
    return get_mods_by_codes(mod_codes=mod_codes)


def _on_request_get_mods_by_ids(
    mod_ids: List[int],
    event: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Returns mods by their IDs.

    :param mod_ids: The IDs of the mods to retrieve.
    :type mod_ids: List[int]
    :param event: The event that triggered the function.
    :type event: Optional[str]

    :return: The mods.
    :rtype: List[Dict[str, Any]]
    """

    # Return the mods
    return get_mods_by_ids(mod_ids=mod_ids)


def _on_request_get_mods_for_game(
    game_id: int,
    event: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Returns mods for a game.

    :param game_id: The ID of the game to retrieve mods for.
    :type game_id: int
    :param event: The event that triggered the function.
    :type event: Optional[str]

    :return: The mods.
    :rtype: List[Dict[str, Any]]
    """

    # Return the mods
    return get_mods_for_game(game_id=game_id)


def _on_request_insert_game(
    name: str,
    path: Union[Path, str],
    event: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Inserts a new game into the database.

    :param name: The name of the game.
    :type name: str
    :param path: The path to the game's directory.
    :type path: Union[Path, str]
    :param event: The event that triggered the function.
    :type event: Optional[str]

    :return: The inserted game.
    :rtype: Optional[Dict[str, Any]]
    """

    # Insert the game
    game_id: Optional[int] = insert_game(
        name=name,
        path=path,
    )

    # Check if the game was inserted
    if game_id is None:
        # Log an exception
        exception(
            exception=Exception("Failed to insert game"),
            message="Failed to insert game",
            name="database.service._on_request_insert_game",
        )

        # Return early
        return None

    # Return the inserted game
    return get_game_by_id(game_id=game_id)


def _on_request_insert_mod(
    game_code: str,
    game_id: int,
    name: str,
    path: Union[Path, str],
    event: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Inserts a new mod into the database.

    :param game_code: The code of the game to which the mod belongs.
    :type game_code: str
    :param game_id: The ID of the game to which the mod belongs.
    :type game_id: int
    :param name: The name of the mod.
    :type name: str
    :param path: The path to the mod's directory.
    :type path: Union[Path, str]
    :param event: The event that triggered the function.
    :type event: Optional[str]

    :return: The inserted mod.
    :rtype: Optional[Dict[str, Any]]
    """

    # Insert the mod
    mod_id: Optional[int] = insert_mod(
        game_code=game_code,
        game_id=game_id,
        name=name,
        path=path,
    )

    # Check if the mod was inserted
    if mod_id is None:
        # Log an exception
        exception(
            exception=Exception("Failed to insert mod"),
            message="Failed to insert mod",
            name="database.service._on_request_insert_mod",
        )

        # Return early
        return None

    # Return the inserted mod
    return get_mod_by_id(mod_id=mod_id)


def _on_request_search_games(
    id: Optional[int] = None,
    code: Optional[str] = None,
    last_loaded_at: Optional[datetime] = None,
    mod_archive_location: Optional[Union[Path, str]] = None,
    mod_install_location: Optional[Union[Path, str]] = None,
    name: Optional[str] = None,
    nexus_id: Optional[str] = None,
    path: Optional[Union[Path, str]] = None,
    registered_at: Optional[datetime] = None,
    event: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Searches for games in the database.

    :param id: The ID of the game to search for.
    :type id: Optional[int]
    :param code: The code of the game to search for.
    :type code: Optional[str]
    :param last_loaded_at: The timestamp when the game was last loaded to search for.
    :type last_loaded_at: Optional[datetime]
    :param mod_archive_location: The mod archive location of the game to search for.
    :type mod_archive_location: Optional[Union[Path, str]]
    :param mod_install_location: The mod install location of the game to search for.
    :type mod_install_location: Optional[Union[Path, str]]
    :param name: The name of the game to search for.
    :type name: Optional[str]
    :param nexus_id: The nexus ID of the game to search for.
    :type nexus_id: Optional[str]
    :param path: The path to the game's directory to search for.
    :type path: Optional[Union[Path, str]]
    :param registered_at: The registered at of the game to search for.
    :type registered_at: Optional[datetime]
    :param event: The event that triggered the function.
    :type event: Optional[str]

    :return: A list of dictionaries containing the games' information.
    :rtype: List[Dict[str, Any]]
    """
    return search_games(
        id=id,
        code=code,
        last_loaded_at=last_loaded_at,
        mod_archive_location=mod_archive_location,
        mod_install_location=mod_install_location,
        name=name,
        nexus_id=nexus_id,
        path=path,
        registered_at=registered_at,
    )


def _on_request_search_mods(
    id: Optional[int] = None,
    code: Optional[str] = None,
    game_code: Optional[str] = None,
    game_id: Optional[int] = None,
    installed: Optional[bool] = None,
    mod_archive_location: Optional[Union[Path, str]] = None,
    mod_install_location: Optional[Union[Path, str]] = None,
    name: Optional[str] = None,
    nexus_id: Optional[str] = None,
    path: Optional[Union[Path, str]] = None,
    registered_at: Optional[datetime] = None,
    symlink_target: Optional[Union[Path, str]] = None,
    symlinks: Optional[Dict[str, str]] = None,
    version: Optional[str] = None,
    event: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Searches for mods in the database.

    :param id: The ID of the mod to search for.
    :type id: Optional[int]
    :param code: The code of the mod to search for.
    :type code: Optional[str]
    :param game_code: The code of the game to search for the mod for.
    :type game_code: Optional[str]
    :param game_id: The ID of the game to search for the mod for.
    :type game_id: Optional[int]
    :param installed: The installed status of the mod to search for.
    :type installed: Optional[bool]
    :param mod_archive_location: The location of the mod's archive to search for.
    :type mod_archive_location: Optional[Union[Path, str]]
    :param mod_install_location: The location of the mod's installation to search for.
    :type mod_install_location: Optional[Union[Path, str]]
    :param name: The name of the mod to search for.
    :type name: Optional[str]
    :param nexus_id: The Nexus ID of the mod to search for.
    :type nexus_id: Optional[str]
    :param path: The path to the mod's directory to search for.
    :type path: Optional[Union[Path, str]]
    :param registered_at: The timestamp when the mod was registered to search for.
    :type registered_at: Optional[datetime]
    :param symlink_target: The target of the mod's symlink to search for.
    :type symlink_target: Optional[Union[Path, str]]
    :param symlinks: The symlinks of the mod to search for.
    :type symlinks: Optional[Dict[str, str]]
    :param version: The version of the mod to search for.
    :type version: Optional[str]
    :param event: The event that triggered the function.
    :type event: Optional[str]

    :return: A list of dictionaries containing the mods' information.
    :rtype: List[Dict[str, Any]]
    """
    return search_mods(
        id=id,
        code=code,
        game_code=game_code,
        game_id=game_id,
        installed=installed,
        mod_archive_location=mod_archive_location,
        mod_install_location=mod_install_location,
        name=name,
        nexus_id=nexus_id,
        path=path,
        registered_at=registered_at,
        symlink_target=symlink_target,
        symlinks=symlinks,
        version=version,
    )


def _on_request_update_game(
    id: int,
    code: Optional[str] = None,
    mod_archive_location: Optional[Union[Path, str]] = None,
    mod_install_location: Optional[Union[Path, str]] = None,
    name: Optional[str] = None,
    nexus_id: Optional[str] = None,
    path: Optional[Union[Path, str]] = None,
    registered_at: Optional[datetime] = None,
    event: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Updates a game in the database.

    :param id: The ID of the game to update.
    :type id: int
    :param code: The code of the game.
    :type code: Optional[str]
    :param mod_archive_location: The mod archive location of the game.
    :type mod_archive_location: Optional[Union[Path, str]]
    :param mod_install_location: The mod install location of the game.
    :type mod_install_location: Optional[Union[Path, str]]
    :param name: The name of the game.
    :type name: Optional[str]
    :param nexus_id: The nexus ID of the game.
    :type nexus_id: Optional[str]
    :param path: The path to the game's directory.
    :type path: Optional[Union[Path, str]]
    :param registered_at: The registered at of the game.
    :type registered_at: Optional[datetime]
    :param event: The event that triggered the function.
    :type event: Optional[str]

    :return: The updated game.
    :rtype: Optional[Dict[str, Any]]
    """

    # Update the game
    update_game(
        id=id,
        code=code,
        mod_archive_location=mod_archive_location,
        mod_install_location=mod_install_location,
        name=name,
        nexus_id=nexus_id,
        path=path,
        registered_at=registered_at,
    )

    # Return the updated game
    return get_game_by_id(game_id=id)


def _on_request_update_mod(
    id: int,
    code: Optional[str] = None,
    game_code: Optional[str] = None,
    game_id: Optional[int] = None,
    installed: Optional[bool] = None,
    mod_archive_location: Optional[Union[Path, str]] = None,
    mod_install_location: Optional[Union[Path, str]] = None,
    name: Optional[str] = None,
    nexus_id: Optional[str] = None,
    path: Optional[Union[Path, str]] = None,
    registered_at: Optional[datetime] = None,
    symlink_target: Optional[Union[Path, str]] = None,
    symlinks: Optional[Dict[str, str]] = None,
    version: Optional[str] = None,
    event: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Updates a mod in the database.

    :param id: The ID of the mod to update.
    :type id: int
    :param code: The code of the mod.
    :type code: Optional[str]
    :param game_code: The code of the game to which the mod belongs.
    :type game_code: Optional[str]
    :param game_id: The ID of the game to which the mod belongs.
    :type game_id: Optional[int]
    :param installed: The installed status of the mod.
    :type installed: Optional[bool]
    :param mod_archive_location: The location of the mod's archive.
    :type mod_archive_location: Optional[Union[Path, str]]
    :param mod_install_location: The location of the mod's installation.
    :type mod_install_location: Optional[Union[Path, str]]
    :param name: The name of the mod.
    :type name: Optional[str]
    :param nexus_id: The nexus ID of the mod.
    :type nexus_id: Optional[str]
    :param path: The path to the mod's directory.
    :type path: Optional[Union[Path, str]]
    :param registered_at: The registered at of the mod.
    :type registered_at: Optional[datetime]
    :param symlink_target: The target of the mod's symlink.
    :type symlink_target: Optional[Union[Path, str]]
    :param symlinks: The symlinks of the mod.
    :type symlinks: Optional[Dict[str, str]]
    :param version: The version of the mod.
    :type version: Optional[str]
    :param event: The event that triggered the function.
    :type event: Optional[str]

    :return: The updated mod.
    :rtype: Optional[Dict[str, Any]]
    """

    # Update the mod
    update_mod(
        id=id,
        code=code,
        game_code=game_code,
        game_id=game_id,
        installed=installed,
        mod_archive_location=mod_archive_location,
        mod_install_location=mod_install_location,
        name=name,
        nexus_id=nexus_id,
        path=path,
        registered_at=registered_at,
        symlink_target=symlink_target,
        symlinks=symlinks,
        version=version,
    )

    # Return the updated mod
    return get_mod_by_id(mod_id=id)


def get_subscriptions() -> List[Dict[str, Any]]:
    """
    Returns the subscriptions.

    :return: The subscriptions.
    :rtype: List[Dict[str, Any]]
    """

    # Declare the subscriptions
    subscriptions: List[Dict[str, Any]] = []

    # Add the subscriptions
    subscriptions.extend(
        [
            {
                "event": "BROADCAST_APPLICATION_SHUTDOWN",
                "function": _on_broadcast_application_shutdown,
                "namespace": "global",
                "persistent": True,
            },
            {
                "event": "REQUEST_GET_ALL_GAMES",
                "function": _on_request_get_all_games,
                "namespace": "global",
                "persistent": True,
            },
            {
                "event": "REQUEST_GET_ALL_MODS",
                "function": _on_request_get_all_mods,
                "namespace": "global",
                "persistent": True,
            },
            {
                "event": "REQUEST_GET_GAME_BY_ID",
                "function": _on_request_get_game_by_id,
                "namespace": "global",
                "persistent": True,
            },
            {
                "event": "REQUEST_GET_GAME_BY_CODE",
                "function": _on_request_get_game_by_code,
                "namespace": "global",
                "persistent": True,
            },
            {
                "event": "REQUEST_GET_GAMES_BY_IDS",
                "function": _on_request_get_games_by_ids,
                "namespace": "global",
                "persistent": True,
            },
            {
                "event": "REQUEST_GET_GAMES_BY_CODES",
                "function": _on_request_get_games_by_codes,
                "namespace": "global",
                "persistent": True,
            },
            {
                "event": "REQUEST_GET_MOD_BY_CODE",
                "function": _on_request_get_mod_by_code,
                "namespace": "global",
                "persistent": True,
            },
            {
                "event": "REQUEST_GET_MOD_BY_ID",
                "function": _on_request_get_mod_by_id,
                "namespace": "global",
                "persistent": True,
            },
            {
                "event": "REQUEST_INSERT_GAME",
                "function": _on_request_insert_game,
                "namespace": "global",
                "persistent": True,
            },
            {
                "event": "REQUEST_INSERT_MOD",
                "function": _on_request_insert_mod,
                "namespace": "global",
                "persistent": True,
            },
            {
                "event": "REQUEST_GET_MODS_BY_CODES",
                "function": _on_request_get_mods_by_codes,
                "namespace": "global",
                "persistent": True,
            },
            {
                "event": "REQUEST_GET_MODS_BY_IDS",
                "function": _on_request_get_mods_by_ids,
                "namespace": "global",
                "persistent": True,
            },
            {
                "event": "REQUEST_GET_MODS_FOR_GAME",
                "function": _on_request_get_mods_for_game,
                "namespace": "global",
                "persistent": True,
            },
            {
                "event": "REQUEST_SEARCH_GAMES",
                "function": _on_request_search_games,
                "namespace": "global",
                "persistent": True,
            },
            {
                "event": "REQUEST_SEARCH_MODS",
                "function": _on_request_search_mods,
                "namespace": "global",
                "persistent": True,
            },
            {
                "event": "REQUEST_UPDATE_GAME",
                "function": _on_request_update_game,
                "namespace": "global",
                "persistent": True,
            },
            {
                "event": "REQUEST_UPDATE_MOD",
                "function": _on_request_update_mod,
                "namespace": "global",
                "persistent": True,
            },
        ]
    )

    # Return the subscriptions
    return subscriptions


def registration_ids() -> List[str]:
    """
    Returns the registration IDs.

    :return: The registration IDs.
    :rtype: List[str]
    """

    # Declare the global variable
    global REGISTRATION_IDS

    # Assert that the registration IDs exist
    assert REGISTRATION_IDS is not None

    # Return the registration IDs
    return REGISTRATION_IDS


def subscribe_to_events() -> None:
    """
    Subscribes to events.

    :return: None
    :rtype: None
    """

    # Declare the global variable
    global REGISTRATION_IDS

    # Assert that the registration IDs exist
    assert REGISTRATION_IDS is not None

    # Iterate over the subscriptions
    for subscription in get_subscriptions():
        # Register the subscription
        registration_id: Union[str, None] = register(
            event=subscription["event"],
            function=subscription["function"],
            namespace=subscription.get(
                "namespace",
                "global",
            ),
            persistent=subscription.get(
                "persistent",
                True,
            ),
        )

        if not registration_id:
            # Log an error message
            exception(
                exception=Exception("Failed to register subscription"),
                message=f"Failed to register subscription: {subscription}",
                name="database.service.subscribe_to_events",
            )

            # Return early
            return

        # Add the registration ID to the registration IDs
        REGISTRATION_IDS.append(registration_id)


def unsubscribe_from_events() -> None:
    """
    Unsubscribes from events.

    :return: None
    :rtype: None
    """

    # Declare the global variable
    global REGISTRATION_IDS

    # Assert that the registration IDs exist
    assert REGISTRATION_IDS is not None

    # Iterate over the registration IDs
    for registration_id in REGISTRATION_IDS:
        # Unregister the registration ID
        unregister(registration_id=registration_id)

    # Clear the registration IDs
    REGISTRATION_IDS.clear()
