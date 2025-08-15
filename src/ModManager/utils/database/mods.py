"""
Author: Louis Goodnews
Date: 2025-08-15
"""

import asyncio
import json
import os

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Final, List, Optional, Union
from uuid import uuid4

from utils.constants import MOD_ARCHIVES_PATH, MOD_INSTALLED_PATH
from utils.database.tables import MODS_TABLE
from utils.logging import exception, info, warn
from utils.sqlite import (
    create_insert_sql_string,
    create_table_sql_string,
    execute_query,
    fetch_all,
    fetch_one,
    get_sqlite_table,
    insert,
    update,
)


__all__: Final[List[str]] = [
    "create_mods_table",
    "get_all_mods",
    "get_mod_by_code",
    "get_mod_by_id",
    "get_mods_by_ids",
    "get_mods_by_codes",
    "get_mods_for_game",
    "insert_mod",
    "update_mod",
]


def create_mods_table() -> None:
    """
    Creates the mods table in the database.

    :return: None
    :rtype: None
    """
    try:
        # Create the table
        asyncio.run(
            execute_query(
                query=create_table_sql_string(
                    table=get_sqlite_table(
                        columns=MODS_TABLE.values(),
                        name="mods",
                    )
                )
            )
        )
    except Exception as e:
        # Log the exception
        exception(
            exception=e,
            message="Failed to create mods table",
            name="mods.create_mods_table",
        )


def get_all_mods() -> List[Dict[str, Any]]:
    """
    Retrieves all mods from the database.

    :return: A list of dictionaries containing the mods' information.
    :rtype: List[Dict[str, Any]]
    """
    try:
        # Prepare the query
        query: str = "SELECT * FROM mods"

        # Fetch all mods
        result: Optional[List[Dict[str, Any]]] = asyncio.run(
            fetch_all(
                query=query,
            )
        )

        # Check if the result is empty
        if not result:
            # Log a warning message
            warn(
                message="No mods found",
                name="mods.get_all_mods",
            )

            # Return an empty list indicating that no mods were found
            return []

        # Return the result as a list of dictionaries
        return [dict(row) for row in result]
    except Exception as e:
        # Log the exception
        exception(
            exception=e,
            message="Failed to fetch all mods",
            name="mods.get_all_mods",
        )

        # Return an empty list indicating that an exception occurred
        return []


def get_mod_by_id(mod_id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieves a mod from the database by its ID.

    :param mod_id: The ID of the mod to retrieve.
    :type mod_id: int

    :return: A dictionary containing the mod's information, or None if not found.
    :rtype: Optional[Dict[str, Any]]
    """
    try:
        # Prepare the query
        query: str = "SELECT * FROM mods WHERE id = ?"

        # Fetch the mod by ID
        result: Optional[Dict[str, Any]] = asyncio.run(
            fetch_one(
                params=[mod_id],
                query=query,
            )
        )

        # Return the result as a dictionary
        return dict(result) if result else None
    except Exception as e:
        # Log the exception
        exception(
            exception=e,
            message=f"Failed to fetch mod with ID {mod_id}",
            name="mods.get_mod_by_id",
        )

        # Return None indicating that an exception occurred
        return None


def get_mods_by_ids(mod_ids: List[int]) -> List[Dict[str, Any]]:
    """
    Retrieves mods from the database by their IDs.

    :param mod_ids: A list of IDs of the mods to retrieve.
    :type mod_ids: List[int]

    :return: A list of dictionaries containing the mods' information.
    :rtype: List[Dict[str, Any]]
    """
    try:
        # Prepare the query
        query: str = "SELECT * FROM mods WHERE id IN ({})".format(
            ", ".join(
                ["?" for _ in mod_ids],
            ),
        )

        # Fetch the mods by IDs
        result: List[Dict[str, Any]] = asyncio.run(
            fetch_all(
                params=mod_ids,
                query=query,
            )
        )

        # Return the result as a list of dictionaries
        return [dict(row) for row in result]
    except Exception as e:
        # Log the exception
        exception(
            exception=e,
            message=f"Failed to fetch mods with IDs {mod_ids}",
            name="mods.get_mods_by_ids",
        )

        # Return an empty list indicating that an exception occurred
        return []


def get_mod_by_code(mod_code: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves a mod from the database by its UUID/code.

    :param mod_code: The UUID/code of the mod to retrieve.
    :type mod_code: str

    :return: A dictionary containing the mod's information, or None if not found.
    :rtype: Optional[Dict[str, Any]]
    """
    try:
        # Prepare the query
        query: str = "SELECT * FROM mods WHERE uuid = ?"

        # Fetch the mod by code
        result: Optional[Dict[str, Any]] = asyncio.run(
            fetch_one(
                params=[mod_code],
                query=query,
            )
        )

        # Return the result as a dictionary
        return dict(result) if result else None
    except Exception as e:
        # Log the exception
        exception(
            exception=e,
            message=f"Failed to fetch mod with code {mod_code}",
            name="mods.get_mod_by_code",
        )

        # Return None indicating that an exception occurred
        return None


def get_mods_by_codes(mod_codes: List[str]) -> List[Dict[str, Any]]:
    """
    Retrieves mods from the database by their UUID/codes.

    :param mod_codes: A list of UUID/codes of the mods to retrieve.
    :type mod_codes: List[str]

    :return: A list of dictionaries containing the mods' information.
    :rtype: List[Dict[str, Any]]
    """
    try:
        # Prepare the query
        query: str = "SELECT * FROM mods WHERE uuid IN ({})".format(
            ", ".join(
                ["?" for _ in mod_codes],
            ),
        )

        # Fetch the mods by codes
        result: List[Dict[str, Any]] = asyncio.run(
            fetch_all(
                params=mod_codes,
                query=query,
            )
        )

        # Return the result as a list of dictionaries
        return [dict(row) for row in result]
    except Exception as e:
        # Log the exception
        exception(
            exception=e,
            message=f"Failed to fetch mods with codes {mod_codes}",
            name="mods.get_mods_by_codes",
        )

        # Return an empty list indicating that an exception occurred
        return []


def get_mods_for_game(game_id: int) -> List[Dict[str, Any]]:
    """
    Retrieves mods from the database for a specific game.

    :param game_id: The ID of the game to retrieve mods for.
    :type game_id: int

    :return: A list of dictionaries containing the mods' information.
    :rtype: List[Dict[str, Any]]
    """
    try:
        # Prepare the query
        query: str = "SELECT * FROM mods WHERE game_id = ?"

        # Fetch the mods for the game
        result: List[Dict[str, Any]] = asyncio.run(
            fetch_all(
                params=[game_id],
                query=query,
            )
        )

        # Check if the result is empty
        if not result:
            # Log a warning message
            warn(
                message=f"No mods found for game with ID {game_id}",
                name="mods.get_mods_for_game",
            )

            # Return an empty list indicating that no mods were found
            return []

        # Return the result as a list of dictionaries
        return [dict(row) for row in result]
    except Exception as e:
        # Log the exception
        exception(
            exception=e,
            message=f"Failed to fetch mods for game with ID {game_id}",
            name="mods.get_mods_for_game",
        )

        # Return an empty list indicating that an exception occurred
        return []


def insert_mod(
    game_code: str,
    game_id: int,
    name: str,
    path: Union[Path, str],
) -> Optional[int]:
    """
    Inserts a new mod into the database.

    :param game: The ID of the game to insert the mod for.
    :type game: int
    :param name: The name of the mod.
    :type name: str
    :param path: The path to the mod's directory.
    :type path: Union[Path, str]

    :return: The ID of the inserted mod.
    :rtype: Optional[int]
    """

    # Check if the path is a Path object
    if not isinstance(
        path,
        Path,
    ):
        # Convert the path to a Path object
        path = Path(path)

    # Generate a random code
    code: str = uuid4().hex

    # Get the current timestamp
    timestamp: datetime = datetime.now().isoformat()

    # Attempt to insert the game into the database
    try:
        # Insert the game
        return asyncio.run(
            insert(
                query=create_insert_sql_string(
                    table=get_sqlite_table(
                        columns=MODS_TABLE.values(),
                        name="mods",
                    )
                ),
                params=[
                    len(get_all_mods()) + 1,
                    code,
                    game_code,
                    game_id,
                    False,
                    path.as_posix(),
                    Path(
                        os.path.join(
                            MOD_INSTALLED_PATH,
                            game_code,
                            code,
                        )
                    ).as_posix(),
                    name,
                    "",
                    "",
                    timestamp,
                    "",
                    "{}",
                    "",
                ],
            )
        )
    except Exception as e:
        # Log the exception
        exception(
            exception=e,
            message=f"Caught an exception while attempting to insert mod with name '{name}' and path '{path}'.",
            name="mods.insert_mod",
        )

        # Return None indicating that an exception occurred
        return None


def search_mods(
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

    :return: A list of dictionaries containing the mods' information.
    :rtype: List[Dict[str, Any]]
    """
    try:
        # Prepare the query
        query: str = "SELECT * FROM mods WHERE "

        # Prepare the parameters
        params: List[Any] = []

        # Add the conditions
        if id:
            query += "id = ? AND "
            params.append(id)

        if code:
            query += "code = ? AND "
            params.append(code)

        if game_code:
            query += "game_code = ? AND "
            params.append(game_code)

        if game_id:
            query += "game_id = ? AND "
            params.append(game_id)

        if installed:
            query += "installed = ? AND "
            params.append(installed)

        if mod_archive_location:
            query += "mod_archive_location = ? AND "
            params.append(mod_archive_location)

        if mod_install_location:
            query += "mod_install_location = ? AND "
            params.append(mod_install_location)

        if name:
            query += "name = ? AND "
            params.append(name)

        if nexus_id:
            query += "nexus_id = ? AND "
            params.append(nexus_id)

        if path:
            query += "path = ? AND "
            params.append(path)

        if registered_at:
            query += "registered_at = ? AND "
            params.append(registered_at)

        if symlink_target:
            query += "symlink_target = ? AND "
            params.append(symlink_target)

        if symlinks:
            query += "symlinks = ? AND "
            params.append(symlinks)

        if version:
            query += "version = ? AND "
            params.append(version)

        # Remove the last "AND"
        query = query[:-5]

        # Fetch the mods
        result: Optional[List[Dict[str, Any]]] = asyncio.run(
            fetch_all(
                query=query,
                params=params,
            )
        )

        # Check if the result is empty
        if not result:
            # Log a warning message
            warn(
                message="No mods found",
                name="mods.search_mods",
            )

            # Return an empty list indicating that no mods were found
            return []

        # Return the result as a list of dictionaries
        return [dict(row) for row in result]
    except Exception as e:
        # Log the exception
        exception(
            exception=e,
            message=f"Failed to fetch mods with parameters {params}",
            name="mods.search_mods",
        )

        # Return an empty list indicating that an exception occurred
        return []


def update_mod(
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
) -> bool:
    """
    Updates a mod in the database.

    :param id: The ID of the mod to update.
    :type id: int
    :param code: The code of the mod to update.
    :type code: Optional[str]
    :param game_code: The code of the game to update the mod for.
    :type game_code: Optional[str]
    :param game_id: The ID of the game to update the mod for.
    :type game_id: Optional[int]
    :param name: The name of the mod to update.
    :type name: Optional[str]
    :param nexus_id: The nexus ID of the mod to update.
    :type nexus_id: Optional[str]
    :param path: The path to the mod's directory to update.
    :type path: Optional[Union[Path, str]]
    :param registered_at: The registered at of the mod to update.
    :type registered_at: Optional[datetime]
    :param version: The version of the mod to update.
    :type version: Optional[str]

    :return: True if the mod was updated, False otherwise.
    :rtype: bool
    """

    # Check if the game exists
    if not asyncio.run(
        fetch_one(
            query="SELECT * FROM mods WHERE id = ?",
            params=[id],
        )
    ):
        # Log a warning message
        warn(
            message=f"Mod with ID '{id}' does not exist",
            name="mods.update_mod",
        )

        # Return False indicating that the mod does not exist
        return False

    # Prepare a dictionary of values to update
    update_values: Dict[str, Any] = {}

    if code is not None:
        update_values["code"] = code
    if game_code is not None:
        update_values["game_code"] = game_code
    if game_id is not None:
        update_values["game_id"] = game_id
    if installed is not None:
        update_values["installed"] = installed
    if mod_archive_location is not None:
        update_values["mod_archive_location"] = (
            Path(path).as_posix()
            if isinstance(
                path,
                (Path, str),
            )
            else path
        )
    if mod_install_location is not None:
        update_values["mod_install_location"] = (
            Path(path).as_posix()
            if isinstance(
                path,
                (Path, str),
            )
            else path
        )
    if name is not None:
        update_values["name"] = name
    if nexus_id is not None:
        update_values["nexus_id"] = nexus_id
    if path is not None:
        update_values["path"] = (
            Path(path).as_posix()
            if isinstance(
                path,
                (Path, str),
            )
            else path
        )
    if registered_at is not None:
        update_values["registered_at"] = (
            registered_at.isoformat()
            if isinstance(
                registered_at,
                datetime,
            )
            else registered_at
        )
    if symlink_target is not None:
        update_values["symlink_target"] = (
            Path(path).as_posix()
            if isinstance(
                path,
                (Path, str),
            )
            else path
        )
    if symlinks is not None:
        update_values["symlinks"] = json.dumps(symlinks)
    if version is not None:
        update_values["version"] = version

    # Return early if nothing to update
    if not update_values:
        return False

    # Dynamically create SET part of the SQL statement
    set_clause: str = ", ".join([f"{key} = ?" for key in update_values.keys()])
    sql: str = f"UPDATE mods SET {set_clause} WHERE id = ?"

    try:
        # Execute the update
        asyncio.run(
            update(
                query=sql,
                params=list(update_values.values()) + [id],
            )
        )

        # Log an info message
        info(
            message=f"Updated mod with ID {id}: {update_values}",
            name="mods.update_mod",
        )

        # Return True indicating that the update was successful
        return True
    except Exception as e:
        # Log an exception
        exception(
            exception=e,
            message=f"Failed to update mod with ID {id}",
            name="mods.update_mod",
        )

        # Return False indicating that the update failed
        return False
