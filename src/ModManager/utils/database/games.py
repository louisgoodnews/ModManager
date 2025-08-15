"""
Author: Louis Goodnews
Date: 2025-08-15
"""

import asyncio
import os

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Final, List, Optional, Union
from uuid import uuid4

from utils.constants import MOD_ARCHIVES_PATH, MOD_INSTALLED_PATH
from utils.database.tables import GAMES_TABLE
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
    "create_games_table",
    "get_all_games",
    "get_game_by_code",
    "get_game_by_id",
    "get_games_by_ids",
    "get_games_by_codes",
    "insert_game",
    "update_game",
]


def create_games_table() -> None:
    """
    Creates the games table in the database.

    :return: None
    :rtype: None
    """
    try:
        # Create the table
        asyncio.run(
            execute_query(
                query=create_table_sql_string(
                    table=get_sqlite_table(
                        columns=GAMES_TABLE.values(),
                        name="games",
                    )
                )
            )
        )
    except Exception as e:
        # Log the exception
        exception(
            exception=e,
            message="Failed to create games table",
            name="games.create_games_table",
        )


def get_all_games() -> List[Dict[str, Any]]:
    """
    Retrieves all games from the database.

    :return: A list of dictionaries containing the games' information.
    :rtype: List[Dict[str, Any]]
    """
    try:
        # Prepare the query
        query: str = "SELECT * FROM games"

        # Fetch all games
        result: List[Dict[str, Any]] = asyncio.run(
            fetch_all(
                query=query,
            )
        )

        # Return the result as a list of dictionaries
        return [dict(row) for row in result]
    except Exception as e:
        # Log the exception
        exception(
            exception=e,
            message="Failed to fetch all games",
            name="games.get_all_games",
        )

        # Return an empty list indicating that an exception occurred
        return []


def get_game_by_id(game_id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieves a game from the database by its ID.

    :param game_id: The ID of the game to retrieve.
    :type game_id: int

    :return: A dictionary containing the game's information, or None if not found.
    :rtype: Optional[Dict[str, Any]]
    """
    try:
        # Prepare the query
        query: str = "SELECT * FROM games WHERE id = ?"

        # Fetch the game by ID
        result: Optional[Dict[str, Any]] = asyncio.run(
            fetch_one(
                params=[game_id],
                query=query,
            )
        )

        # Return the result as a dictionary
        return dict(result) if result else None
    except Exception as e:
        # Log the exception
        exception(
            exception=e,
            message=f"Failed to fetch game with ID {game_id}",
            name="games.get_game_by_id",
        )

        # Return None indicating that an exception occurred
        return None


def get_games_by_ids(game_ids: List[int]) -> List[Dict[str, Any]]:
    """
    Retrieves games from the database by their IDs.

    :param game_ids: A list of IDs of the games to retrieve.
    :type game_ids: List[int]

    :return: A list of dictionaries containing the games' information.
    :rtype: List[Dict[str, Any]]
    """
    try:
        # Prepare the query
        query: str = "SELECT * FROM games WHERE id IN ({})".format(
            ", ".join(
                ["?" for _ in game_ids],
            ),
        )

        # Fetch the games by IDs
        result: List[Dict[str, Any]] = asyncio.run(
            fetch_all(
                params=game_ids,
                query=query,
            )
        )

        # Return the result as a list of dictionaries
        return [dict(row) for row in result]
    except Exception as e:
        # Log the exception
        exception(
            exception=e,
            message=f"Failed to fetch games with IDs {game_ids}",
            name="games.get_games_by_ids",
        )

        # Return an empty list indicating that an exception occurred
        return []


def get_game_by_code(game_code: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves a game from the database by its UUID/code.

    :param game_code: The UUID/code of the game to retrieve.
    :type game_code: str

    :return: A dictionary containing the game's information, or None if not found.
    :rtype: Optional[Dict[str, Any]]
    """
    try:
        # Prepare the query
        query: str = "SELECT * FROM games WHERE uuid = ?"

        # Fetch the game by code
        result: Optional[Dict[str, Any]] = asyncio.run(
            fetch_one(
                params=[game_code],
                query=query,
            )
        )

        # Return the result as a dictionary
        return dict(result) if result else None
    except Exception as e:
        # Log the exception
        exception(
            exception=e,
            message=f"Failed to fetch game with code {game_code}",
            name="games.get_game_by_code",
        )

        # Return None indicating that an exception occurred
        return None


def get_games_by_codes(game_codes: List[str]) -> List[Dict[str, Any]]:
    """
    Retrieves games from the database by their UUID/codes.

    :param game_codes: A list of UUID/codes of the games to retrieve.
    :type game_codes: List[str]

    :return: A list of dictionaries containing the games' information.
    :rtype: List[Dict[str, Any]]
    """
    try:
        # Prepare the query
        query: str = "SELECT * FROM games WHERE uuid IN ({})".format(
            ", ".join(
                ["?" for _ in game_codes],
            ),
        )

        # Fetch the games by codes
        result: List[Dict[str, Any]] = asyncio.run(
            fetch_all(
                params=game_codes,
                query=query,
            )
        )

        # Return the result as a list of dictionaries
        return [dict(row) for row in result]
    except Exception as e:
        # Log the exception
        exception(
            exception=e,
            message=f"Failed to fetch games with codes {game_codes}",
            name="games.get_games_by_codes",
        )

        # Return an empty list indicating that an exception occurred
        return []


def insert_game(
    name: str,
    path: Union[Path, str],
) -> Optional[int]:
    """
    Inserts a new game into the database.

    :param name: The name of the game.
    :type name: str
    :param path: The path to the game's directory.
    :type path: Union[Path, str]

    :return: The ID of the inserted game.
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
                query=create_insert_sql_string(table=GAMES_TABLE),
                params=[
                    code,
                    timestamp,
                    Path(
                        os.path.join(
                            MOD_ARCHIVES_PATH,
                            code,
                        )
                    ).as_posix(),
                    Path(
                        os.path.join(
                            MOD_INSTALLED_PATH,
                            code,
                        )
                    ).as_posix(),
                    name,
                    name.replace(" ", "_").lower(),
                    path.as_posix(),
                    timestamp,
                ],
            )
        )
    except Exception as e:
        # Log the exception
        exception(
            exception=e,
            message=f"Caught an exception while attempting to insert game with name '{name}' and path '{path}'.",
            name="games.insert_game",
        )

        # Return None indicating that an exception occurred
        return None


def search_games(
    id: Optional[int] = None,
    code: Optional[str] = None,
    last_loaded_at: Optional[datetime] = None,
    mod_archive_location: Optional[Union[Path, str]] = None,
    mod_install_location: Optional[Union[Path, str]] = None,
    name: Optional[str] = None,
    nexus_id: Optional[str] = None,
    path: Optional[Union[Path, str]] = None,
    registered_at: Optional[datetime] = None,
) -> List[Dict[str, Any]]:
    """
    Searches for games in the database based on the provided parameters.

    :param id: The ID of the game to search for.
    :type id: Optional[int]
    :param code: The code of the game to search for.
    :type code: Optional[str]
    :param last_loaded_at: The last loaded at of the game to search for.
    :type last_loaded_at: Optional[datetime]
    :param mod_archive_location: The mod archive location of the game to search for.
    :type mod_archive_location: Optional[Union[Path, str]]
    :param mod_install_location: The mod install location of the game to search for.
    :type mod_install_location: Optional[Union[Path, str]]
    :param name: The name of the game to search for.
    :type name: Optional[str]
    :param nexus_id: The nexus ID of the game to search for.
    :type nexus_id: Optional[str]
    :param path: The path of the game to search for.
    :type path: Optional[Union[Path, str]]
    :param registered_at: The registered at of the game to search for.
    :type registered_at: Optional[datetime]

    :return: A list of dictionaries containing the games' information.
    :rtype: List[Dict[str, Any]]
    """
    try:
        # Prepare the query
        query: str = "SELECT * FROM games WHERE id = ?"

        # Fetch the games by ID
        result: List[Dict[str, Any]] = asyncio.run(
            fetch_all(
                params=[id],
                query=query,
            )
        )

        # Return the result as a list of dictionaries
        return [dict(row) for row in result]
    except Exception as e:
        # Log the exception
        exception(
            exception=e,
            message=f"Failed to fetch games with ID {id}",
            name="games.get_game_by_id",
        )

        # Return an empty list indicating that an exception occurred
        return []


def update_game(
    id: int,
    code: Optional[str] = None,
    last_loaded_at: Optional[datetime] = None,
    mod_archive_location: Optional[Union[Path, str]] = None,
    mod_install_location: Optional[Union[Path, str]] = None,
    name: Optional[str] = None,
    nexus_id: Optional[str] = None,
    path: Optional[Union[Path, str]] = None,
    registered_at: Optional[datetime] = None,
) -> bool:
    """
    Updates a game in the database.

    :param id: The ID of the game to update.
    :type id: int
    :param code: The code of the game to update.
    :type code: Optional[str]
    :param last_loaded_at: The last loaded at of the game to update.
    :type last_loaded_at: Optional[datetime]
    :param mod_archive_location: The mod archive location of the game to update.
    :type mod_archive_location: Optional[Union[Path, str]]
    :param mod_install_location: The mod install location of the game to update.
    :type mod_install_location: Optional[Union[Path, str]]
    :param name: The name of the game to update.
    :type name: Optional[str]
    :param nexus_id: The nexus ID of the game to update.
    :type nexus_id: Optional[str]
    :param path: The path of the game to update.
    :type path: Optional[Union[Path, str]]
    :param registered_at: The registered at of the game to update.
    :type registered_at: Optional[datetime]

    :return: True if the update was successful, False otherwise.
    :rtype: bool
    """

    # Check if the game exists
    if not asyncio.run(
        fetch_one(
            query="SELECT * FROM games WHERE id = ?",
            params=[id],
        )
    ):
        # Log a warning message
        warn(
            message=f"Game with ID '{id}' does not exist",
            name="games.update_game",
        )

        # Return False indicating that the game does not exist
        return False

    # Prepare a dictionary of values to update
    update_values: Dict[str, Any] = {}

    if code is not None:
        update_values["uuid"] = code
    if last_loaded_at is not None:
        update_values["last_loaded_at"] = (
            last_loaded_at.isoformat()
            if isinstance(
                last_loaded_at,
                datetime,
            )
            else last_loaded_at
        )
    if mod_archive_location is not None:
        update_values["mod_folder_location"] = (
            Path(mod_archive_location).as_posix()
            if isinstance(
                mod_archive_location,
                (Path, str),
            )
            else mod_archive_location
        )
    if mod_install_location is not None:
        update_values["mod_folder_location"] = (
            Path(mod_install_location).as_posix()
            if isinstance(
                mod_install_location,
                (Path, str),
            )
            else mod_install_location
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

    # Return early if nothing to update
    if not update_values:
        return False

    # Dynamically create SET part of the SQL statement
    set_clause: str = ", ".join([f"{key} = ?" for key in update_values.keys()])
    sql: str = f"UPDATE games SET {set_clause} WHERE id = ?"

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
            message=f"Updated game with ID {id}: {update_values}",
            name="games.update_game",
        )

        # Return True indicating that the update was successful
        return True
    except Exception as e:
        # Log an exception
        exception(
            exception=e,
            message=f"Failed to update game with ID {id}",
            name="games.update_game",
        )

        # Return False indicating that the update failed
        return False
