"""
Author: Louis Goodnews
Date: 2025-08-12
"""

import os

from pathlib import Path
from typing import Any, Dict, Final, List, Union

from utils.files import create_directory, file_read_json, file_write_json
from utils.logging import exception, info


__all__: Final[List[str]] = [
    "API_JSON",
    "create_mod_staging_folder_for_game",
    "load_api_json",
    "write_api_json",
]


API_JSON: Final[Dict[str, Any]] = {}

API_JSON_PATH: Final[Path] = Path(
    os.path.join(
        os.getcwd(),
        "api.json",
    )
)


def create_mod_staging_folder_for_game(
    game: str,
    path: Union[Path, str],
) -> bool:
    """
    Creates a mod staging folder for the specified game.

    :param game: The name of the game.
    :type game: str
    :param path: The path to the mod staging folder.
    :type path: Union[Path, str]

    :return: True if the mod staging folder was created successfully, False otherwise.
    :rtype: bool

    :raises Exception: If the mod staging folder could not be created.
    """

    # Check if the path is a Path object
    if not isinstance(
        path,
        Path,
    ):
        # Convert the path to a Path object
        path = Path(path)

    try:
        # Create the mod staging folder
        create_directory(
            path=path.joinpath(
                game,
                "staging",
            )
        )

        # Log mod staging folder creation
        info(
            message=f"Created mod staging folder for game '{game}' at '{path}'",
            name="core.create_mod_staging_folder_for_game",
        )

        # Return True
        return True
    except Exception as e:
        # Log an exception
        exception(
            exception=e,
            message="Failed to create mod staging folder for game. Aborting.",
            name="core.create_mod_staging_folder_for_game",
        )

        # Return False
        return False


def load_api_json() -> None:
    """
    Loads the API JSON file.

    :return: None
    :rtype: None
    """

    # Check if the API JSON file exists
    if not API_JSON_PATH.exists():
        # Log an exception
        exception(
            exception=FileNotFoundError("'api.json' file not found."),
            message="Failed to load 'api.json' file. Aborting.",
            name="core.load_api_json",
        )

        # Return early
        return

    # Load the API JSON file
    API_JSON.update(file_read_json(path=API_JSON_PATH))

    # Log API JSON file loading
    info(
        message=f"Loaded API JSON file at '{API_JSON_PATH}'",
        name="core.load_api_json",
    )


def write_api_json(
    **kwargs,
) -> bool:
    """
    Writes the API JSON file.

    :param kwargs: Keyword arguments to write to the API JSON file.
    :type kwargs: Dict[str, Any]

    :return: True if the API JSON file was written successfully, False otherwise.
    :rtype: bool
    """

    # Load the api.json file
    load_api_json()

    # Update the API JSON file
    API_JSON.update(kwargs)

    try:
        # Write the API JSON file
        file_write_json(
            path=API_JSON_PATH,
            data=API_JSON,
        )

        # Log API JSON file writing
        info(
            message=f"Wrote API JSON file at '{API_JSON_PATH}'",
            name="core.write_api_json",
        )

        # Return True
        return True
    except Exception as e:
        # Log an exception
        exception(
            exception=e,
            message="Failed to write 'api.json' file. Aborting.",
            name="core.write_api_json",
        )

        # Return False
        return False
