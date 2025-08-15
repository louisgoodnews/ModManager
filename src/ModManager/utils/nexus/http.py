"""
Author: Louis Goodnews
Date: 2025-08-11
"""

from typing import Any, Dict, Final, List, Literal, Optional

from utils.logging import exception
from utils.http import http_delete, http_get, http_post


__all__: Final[List[str]] = [
    "abstain_edorsing_mod",
    "endorse_mod",
    "get_all_endorsements",
    "get_all_games",
    "get_all_tracked_mods",
    "get_game",
    "get_latest_added_mods",
    "get_latest_updated_mods",
    "get_mod",
    "get_mod_changelogs",
    "get_mod_download_link",
    "get_mod_file",
    "get_mod_files",
    "get_trending_mods",
    "get_updated_mods",
    "track_mod",
    "untrack_mod",
    "validate_api_key",
]


def abstain_edorsing_mod(
    api_key: str,
    game: str,
    mod_id: int,
) -> Dict[str, Any]:
    """
    Performs an asynchronous GET request to the Nexus API
    to abstain from endorsing a specific mod.

    :param api_key: The API key to use for authentication.
    :type api_key: str
    :param game: The name of the game to abstain from endorsing the mod for.
    :type game: str
    :param mod_id: The ID of the mod to abstain from endorsing.
    :type mod_id: int

    :return: A dictionary containing information about the abstained mod.
    :rtype: Dict[str, Any]

    :raises Exception: If the response is not OK.
    """

    # Send a GET request to the Nexus Abstain Endorse Mod API
    response: Optional[Dict[str, Any]] = http_post(
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "apikey": api_key,
        },
        url=f"https://api.nexusmods.com/v1/games/{game.lower()}/mods/{mod_id}/abstain.json",
    )

    # Check if the response exists
    if not response:
        # Log the exception
        exception(
            exception=Exception("Failed to abstain from endorsing mod"),
            message="Failed to abstain from endorsing mod",
            name="nexus.abstain_edorsing_mod",
        )

        # Return an empty dictionary if the response is not OK
        return {}

    # Check if the response is OK
    if response.get("reason") == "OK":
        # Return the abstained mod information
        return response.get("body", {})
    else:
        # Log the exception
        exception(
            exception=Exception(response.get("reason")),
            message="Failed to abstain from endorsing mod",
            name="nexus.abstain_edorsing_mod",
        )

    # Return an empty dictionary if the response is not OK
    return {}


def endorse_mod(
    api_key: str,
    game: str,
    mod_id: int,
) -> Dict[str, Any]:
    """
    Performs an asynchronous GET request to the Nexus API
    to endorse a specific mod.

    :param api_key: The API key to use for authentication.
    :type api_key: str
    :param game: The name of the game to endorse the mod for.
    :type game: str
    :param mod_id: The ID of the mod to endorse.
    :type mod_id: int

    :return: A dictionary containing information about the endorsed mod.
    :rtype: Dict[str, Any]

    :raises Exception: If the response is not OK.
    """

    # Send a GET request to the Nexus Endorse Mod API
    response: Optional[Dict[str, Any]] = http_post(
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "apikey": api_key,
        },
        url=f"https://api.nexusmods.com/v1/games/{game.lower()}/mods/{mod_id}/endorse.json",
    )

    # Check if the response exists
    if not response:
        # Log the exception
        exception(
            exception=Exception("Failed to endorse mod"),
            message="Failed to endorse mod",
            name="nexus.endorse_mod",
        )

        # Return an empty dictionary if the response is not OK
        return {}

    # Check if the response is OK
    if response.get("reason") == "OK":
        # Return the endorsed mod information
        return response.get("body", {})
    else:
        # Log the exception
        exception(
            exception=Exception(response.get("reason")),
            message="Failed to endorse mod",
            name="nexus.endorse_mod",
        )

    # Return an empty dictionary if the response is not OK
    return {}


def get_all_endorsements(
    api_key: str,
) -> List[Dict[str, Any]]:
    """
    Performs an asynchronous GET request to the Nexus API
    to retrieve a list of all endorsements.

    :param api_key: The API key to use for authentication.
    :type api_key: str

    :return: A list of dictionaries containing information about endorsements.
    :rtype: List[Dict[str, Any]]

    :raises Exception: If the response is not OK.
    """

    # Send a GET request to the Nexus Endorsements API
    response: Optional[Dict[str, Any]] = http_get(
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "apikey": api_key,
        },
        url="https://api.nexusmods.com/v1/users/endorsements.json",
    )

    # Check if the response exists
    if not response:
        # Log the exception
        exception(
            exception=Exception("Failed to get all endorsements"),
            message="Failed to get all endorsements",
            name="nexus.get_all_endorsements",
        )

        # Return an empty list if the response is not OK
        return []

    # Check if the response is OK
    if response.get("reason") == "OK":
        # Return the list of endorsements
        return response.get("body", [])
    else:
        # Log the exception
        exception(
            exception=Exception(response.get("reason")),
            message="Failed to get all endorsements",
            name="nexus.get_all_endorsements",
        )

    # Return an empty list if the response is not OK
    return []


def get_all_games(api_key: str) -> List[Dict[str, Any]]:
    """
    Performs an asynchronous GET request to the Nexus API
    to retrieve a list of all games.

    :param api_key: The API key to use for authentication.
    :type api_key: str

    :return: A list of dictionaries containing information about available games.
    :rtype: List[Dict[str, Any]]

    :raises Exception: If the response is not OK.
    """

    # Send a GET request to the Nexus Games API
    response: Optional[Dict[str, Any]] = http_get(
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "apikey": api_key,
        },
        url="https://api.nexusmods.com/v1/games.json",
    )

    # Check if the response exists
    if not response:
        # Log the exception
        exception(
            exception=Exception("Failed to get all games"),
            message="Failed to get all games",
            name="nexus.get_all_games",
        )

        # Return an empty list if the response is not OK
        return []

    # Check if the response is OK
    if response.get("reason") == "OK":
        # Return the list of games
        return response.get("body", [])
    else:
        # Log the exception
        exception(
            exception=Exception(response.get("reason")),
            message="Failed to get all games",
            name="nexus.get_all_games",
        )

    # Return an empty list if the response is not OK
    return []


def get_all_tracked_mods(
    api_key: str,
) -> List[Dict[str, Any]]:
    """
    Performs an asynchronous GET request to the Nexus API
    to retrieve a list of all tracked mods.

    :param api_key: The API key to use for authentication.
    :type api_key: str

    :return: A list of dictionaries containing information about tracked mods.
    :rtype: List[Dict[str, Any]]

    :raises Exception: If the response is not OK.
    """

    # Send a GET request to the Nexus Tracked Mods API
    response: Optional[Dict[str, Any]] = http_get(
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "apikey": api_key,
        },
        url="https://api.nexusmods.com/v1/users/tracked_mods.json",
    )

    # Check if the response exists
    if not response:
        # Log the exception
        exception(
            exception=Exception("Failed to get all tracked mods"),
            message="Failed to get all tracked mods",
            name="nexus.get_all_tracked_mods",
        )

        # Return an empty list if the response is not OK
        return []

    # Check if the response is OK
    if response.get("reason") == "OK":
        # Return the list of tracked mods
        return response.get("body", [])
    else:
        # Log the exception
        exception(
            exception=Exception(response.get("reason")),
            message="Failed to get all tracked mods",
            name="nexus.get_all_tracked_mods",
        )

    # Return an empty list if the response is not OK
    return []


def get_game(
    api_key: str,
    game: str,
) -> Dict[str, Any]:
    """
    Performs an asynchronous GET request to the Nexus API
    to retrieve information about a specific game.

    :param api_key: The API key to use for authentication.
    :type api_key: str
    :param game: The name of the game to retrieve information about.
    :type game: str

    :return: A dictionary containing information about the specified game.
    :rtype: Dict[str, Any]

    :raises Exception: If the response is not OK.
    """

    # Send a GET request to the Nexus Game API
    response: Optional[Dict[str, Any]] = http_get(
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "apikey": api_key,
        },
        url=f"https://api.nexusmods.com/v1/games/{game.lower()}.json",
    )

    # Check if the response exists
    if not response:
        # Log the exception
        exception(
            exception=Exception("Failed to get game information"),
            message="Failed to get game information",
            name="nexus.get_game",
        )

        # Return an empty dictionary if the response is not OK
        return {}

    # Check if the response is OK
    if response.get("reason") == "OK":
        # Return the game information
        return response.get("body", {})
    else:
        # Log the exception
        exception(
            exception=Exception(response.get("reason")),
            message="Failed to get game information",
            name="nexus.get_game",
        )

    # Return an empty dictionary if the response is not OK
    return {}


def get_latest_added_mods(
    api_key: str,
    game: str,
) -> List[Dict[str, Any]]:
    """
    Performs an asynchronous GET request to the Nexus API
    to retrieve a list of latest added mods for a specific game.

    :param api_key: The API key to use for authentication.
    :type api_key: str
    :param game: The name of the game to retrieve latest added mods for.
    :type game: str

    :return: A list of dictionaries containing information about the latest added mods.
    :rtype: List[Dict[str, Any]]

    :raises Exception: If the response is not OK.
    """

    # Send a GET request to the Nexus Latest Added Mods API
    response: Optional[Dict[str, Any]] = http_get(
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "apikey": api_key,
        },
        url=f"https://api.nexusmods.com/v1/games/{game.lower()}/mods/latest_added.json",
    )

    # Check if the response exists
    if not response:
        # Log the exception
        exception(
            exception=Exception("Failed to get latest added mods"),
            message="Failed to get latest added mods",
            name="nexus.get_latest_added_mods",
        )

        # Return an empty list if the response is not OK
        return []

    # Check if the response is OK
    if response.get("reason") == "OK":
        # Return the list of latest added mods
        return response.get("body", [])
    else:
        # Log the exception
        exception(
            exception=Exception(response.get("reason")),
            message="Failed to get latest added mods",
            name="nexus.get_latest_added_mods",
        )

    # Return an empty list if the response is not OK
    return []


def get_latest_updated_mods(
    api_key: str,
    game: str,
) -> List[Dict[str, Any]]:
    """
    Performs an asynchronous GET request to the Nexus API
    to retrieve a list of latest updated mods for a specific game.

    :param api_key: The API key to use for authentication.
    :type api_key: str
    :param game: The name of the game to retrieve latest updated mods for.
    :type game: str

    :return: A list of dictionaries containing information about the latest updated mods.
    :rtype: List[Dict[str, Any]]

    :raises Exception: If the response is not OK.
    """

    # Send a GET request to the Nexus Latest Updated Mods API
    response: Optional[Dict[str, Any]] = http_get(
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "apikey": api_key,
        },
        url=f"https://api.nexusmods.com/v1/games/{game.lower()}/mods/latest_updated.json",
    )

    # Check if the response exists
    if not response:
        # Log the exception
        exception(
            exception=Exception("Failed to get latest updated mods"),
            message="Failed to get latest updated mods",
            name="nexus.get_latest_updated_mods",
        )

        # Return an empty list if the response is not OK
        return []

    # Check if the response is OK
    if response.get("reason") == "OK":
        # Return the list of latest updated mods
        return response.get("body", [])
    else:
        # Log the exception
        exception(
            exception=Exception(response.get("reason")),
            message="Failed to get latest updated mods",
            name="nexus.get_latest_updated_mods",
        )

    # Return an empty list if the response is not OK
    return []


def get_mod(
    api_key: str,
    game: str,
    mod_id: int,
) -> Dict[str, Any]:
    """
    Performs an asynchronous GET request to the Nexus API
    to retrieve information about a specific mod.

    :param api_key: The API key to use for authentication.
    :type api_key: str
    :param game: The name of the game to retrieve mod information for.
    :type game: str
    :param mod_id: The ID of the mod to retrieve information for.
    :type mod_id: int

    :return: A dictionary containing information about the specified mod.
    :rtype: Dict[str, Any]

    :raises Exception: If the response is not OK.
    """

    # Send a GET request to the Nexus Mod API
    response: Optional[Dict[str, Any]] = http_get(
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "apikey": api_key,
        },
        url=f"https://api.nexusmods.com/v1/games/{game.lower()}/mods/{mod_id}.json",
    )

    # Check if the response exists
    if not response:
        # Log the exception
        exception(
            exception=Exception("Failed to get mod information"),
            message="Failed to get mod information",
            name="nexus.get_mod",
        )

        # Return an empty dictionary if the response is not OK
        return {}

    # Check if the response is OK
    if response.get("reason") == "OK":
        # Return the mod information
        return response.get("body", {})
    else:
        # Log the exception
        exception(
            exception=Exception(response.get("reason")),
            message="Failed to get mod information",
            name="nexus.get_mod",
        )

    # Return an empty dictionary if the response is not OK
    return {}


def get_mod_changelogs(
    api_key: str,
    game: str,
    mod_id: int,
) -> List[Dict[str, Any]]:
    """
    Performs an asynchronous GET request to the Nexus API
    to retrieve a list of changelogs for a specific mod.

    :param api_key: The API key to use for authentication.
    :type api_key: str
    :param game: The name of the game to retrieve changelogs for.
    :type game: str
    :param mod_id: The ID of the mod to retrieve changelogs for.
    :type mod_id: int

    :return: A list of dictionaries containing information about the changelogs.
    :rtype: List[Dict[str, Any]]

    :raises Exception: If the response is not OK.
    """

    # Send a GET request to the Nexus Mod Changelogs API
    response: Optional[Dict[str, Any]] = http_get(
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "apikey": api_key,
        },
        url=f"https://api.nexusmods.com/v1/games/{game.lower()}/mods/{mod_id}/changelogs.json",
    )

    # Check if the response exists
    if not response:
        # Log the exception
        exception(
            exception=Exception("Failed to get mod changelogs"),
            message="Failed to get mod changelogs",
            name="nexus.get_mod_changelogs",
        )

        # Return an empty list if the response is not OK
        return []

    # Check if the response is OK
    if response.get("reason") == "OK":
        # Return the list of changelogs
        return response.get("body", [])
    else:
        # Log the exception
        exception(
            exception=Exception(response.get("reason")),
            message="Failed to get mod changelogs",
            name="nexus.get_mod_changelogs",
        )

    # Return an empty list if the response is not OK
    return []


def get_mod_download_link(
    api_key: str,
    file_id: int,
    game: str,
    mod_id: int,
) -> Dict[str, Any]:
    """
    Performs an asynchronous GET request to the Nexus API
    to retrieve a download link for a specific file for a specific mod.

    :param api_key: The API key to use for authentication.
    :type api_key: str
    :param file_id: The ID of the file to retrieve a download link for.
    :type file_id: int
    :param game: The name of the game to retrieve a download link for.
    :type game: str
    :param mod_id: The ID of the mod to retrieve a download link for.
    :type mod_id: int

    :return: A dictionary containing information about the download link.
    :rtype: Dict[str, Any]

    :raises Exception: If the response is not OK.
    """

    # Send a GET request to the Nexus Mod Download Link API
    response: Optional[Dict[str, Any]] = http_get(
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "apikey": api_key,
        },
        url=f"https://api.nexusmods.com/v1/games/{game.lower()}/mods/{mod_id}/files/{file_id}/download_link.json",
    )

    # Check if the response exists
    if not response:
        # Log the exception
        exception(
            exception=Exception("Failed to get mod download link"),
            message="Failed to get mod download link",
            name="nexus.get_mod_download_link",
        )

        # Return an empty dictionary if the response is not OK
        return {}

    # Check if the response is OK
    if response.get("reason") == "OK":
        # Return the download link
        return response.get("body", {})
    else:
        # Log the exception
        exception(
            exception=Exception(response.get("reason")),
            message="Failed to get mod download link",
            name="nexus.get_mod_download_link",
        )

    # Return an empty dictionary if the response is not OK
    return {}


def get_mod_file(
    api_key: str,
    file_id: int,
    game: str,
    mod_id: int,
) -> Dict[str, Any]:
    """
    Performs an asynchronous GET request to the Nexus API
    to retrieve information about a specific file for a specific mod.

    :param api_key: The API key to use for authentication.
    :type api_key: str
    :param file_id: The ID of the file to retrieve information for.
    :type file_id: int
    :param game: The name of the game to retrieve file information for.
    :type game: str
    :param mod_id: The ID of the mod to retrieve file information for.
    :type mod_id: int

    :return: A dictionary containing information about the specified file.
    :rtype: Dict[str, Any]

    :raises Exception: If the response is not OK.
    """

    # Send a GET request to the Nexus Mod File API
    response: Optional[Dict[str, Any]] = http_get(
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "apikey": api_key,
        },
        url=f"https://api.nexusmods.com/v1/games/{game.lower()}/mods/{mod_id}/files/{file_id}.json",
    )

    # Check if the response exists
    if not response:
        # Log the exception
        exception(
            exception=Exception("Failed to get mod file information"),
            message="Failed to get mod file information",
            name="nexus.get_mod_file",
        )

        # Return an empty dictionary if the response is not OK
        return {}

    # Check if the response is OK
    if response.get("reason") == "OK":
        # Return the file information
        return response.get("body", {})
    else:
        # Log the exception
        exception(
            exception=Exception(response.get("reason")),
            message="Failed to get mod file information",
            name="nexus.get_mod_file",
        )

    # Return an empty dictionary if the response is not OK
    return {}


def get_mod_files(
    api_key: str,
    game: str,
    mod_id: int,
) -> List[Dict[str, Any]]:
    """
    Performs an asynchronous GET request to the Nexus API
    to retrieve a list of files for a specific mod.

    :param api_key: The API key to use for authentication.
    :type api_key: str
    :param game: The name of the game to retrieve files for.
    :type game: str
    :param mod_id: The ID of the mod to retrieve files for.
    :type mod_id: int

    :return: A list of dictionaries containing information about the files.
    :rtype: List[Dict[str, Any]]

    :raises Exception: If the response is not OK.
    """

    # Send a GET request to the Nexus Mod Files API
    response: Optional[Dict[str, Any]] = http_get(
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "apikey": api_key,
        },
        url=f"https://api.nexusmods.com/v1/games/{game.lower()}/mods/{mod_id}/files.json",
    )

    # Check if the response exists
    if not response:
        # Log the exception
        exception(
            exception=Exception("Failed to get mod files"),
            message="Failed to get mod files",
            name="nexus.get_mod_files",
        )

        # Return an empty list if the response is not OK
        return []

    # Check if the response is OK
    if response.get("reason") == "OK":
        # Return the list of files
        return response.get("body", [])
    else:
        # Log the exception
        exception(
            exception=Exception(response.get("reason")),
            message="Failed to get mod files",
            name="nexus.get_mod_files",
        )

    # Return an empty list if the response is not OK
    return []


def get_trending_mods(
    api_key: str,
    games: str,
) -> List[Dict[str, Any]]:
    """
    Performs an asynchronous GET request to the Nexus API
    to retrieve a list of trending mods for a specific game.

    :param api_key: The API key to use for authentication.
    :type api_key: str
    :param games: The name of the game to retrieve trending mods for.
    :type games: str

    :return: A list of dictionaries containing information about trending mods.
    :rtype: List[Dict[str, Any]]

    :raises Exception: If the response is not OK.
    """

    # Send a GET request to the Nexus Trending Mods API
    response: Optional[Dict[str, Any]] = http_get(
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "apikey": api_key,
        },
        url=f"https://api.nexusmods.com/v1/games/{games}/mods/trending.json",
    )

    # Check if the response exists
    if not response:
        # Log the exception
        exception(
            exception=Exception("Failed to get trending mods"),
            message="Failed to get trending mods",
            name="nexus.get_trending_mods",
        )

        # Return an empty list if the response is not OK
        return []

    # Check if the response is OK
    if response.get("reason") == "OK":
        # Return the list of trending mods
        return response.get("body", [])
    else:
        # Log the exception
        exception(
            exception=Exception(response.get("reason")),
            message="Failed to get trending mods",
            name="nexus.get_trending_mods",
        )

    # Return an empty list if the response is not OK
    return []


def get_updated_mods(
    api_key: str,
    game: str,
    period: Optional[Literal["1d", "1w", "1m"]] = None,
) -> List[Dict[str, Any]]:
    """
    Performs an asynchronous GET request to the Nexus API
    to retrieve a list of updated mods for a specific game.

    :param api_key: The API key to use for authentication.
    :type api_key: str
    :param game: The name of the game to retrieve updated mods for.
    :type game: str
    :param period: The period to retrieve updated mods for.
    :type period: Optional[Literal["1d", "1w", "1m"]] = None

    :return: A list of dictionaries containing information about updated mods.
    :rtype: List[Dict[str, Any]]

    :raises Exception: If the response is not OK.
    """

    # Send a GET request to the Nexus Updated Mods API
    response: Optional[Dict[str, Any]] = http_get(
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "apikey": api_key,
        },
        url=f"https://api.nexusmods.com/v1/games/{game.lower()}/mods/updated{f'?period={period}' if period else ''}.json",
    )

    # Check if the response exists
    if not response:
        # Log the exception
        exception(
            exception=Exception("Failed to get updated mods"),
            message="Failed to get updated mods",
            name="nexus.get_updated_mods",
        )

        # Return an empty list if the response is not OK
        return []

    # Check if the response is OK
    if response.get("reason") == "OK":
        # Return the list of updated mods
        return response.get("body", [])
    else:
        # Log the exception
        exception(
            exception=Exception(response.get("reason")),
            message="Failed to get updated mods",
            name="nexus.get_updated_mods",
        )

    # Return an empty list if the response is not OK
    return []


def track_mod(
    api_key: str,
    game: str,
    mod_id: int,
) -> Dict[str, Any]:
    """
    Performs an asynchronous GET request to the Nexus API
    to track a specific mod for a specific game.

    :param api_key: The API key to use for authentication.
    :type api_key: str
    :param game: The name of the game to track a mod for.
    :type game: str
    :param mod_id: The ID of the mod to track.
    :type mod_id: int

    :return: A dictionary containing information about the tracked mod.
    :rtype: Dict[str, Any]

    :raises Exception: If the response is not OK.
    """

    # Send a GET request to the Nexus Track Mod API
    response: Optional[Dict[str, Any]] = http_post(
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "apikey": api_key,
        },
        params={
            "game": game,
            "mod_id": mod_id,
        },
        url="https://api.nexusmods.com/v1/users/tracked_mods.json",
    )

    # Check if the response exists
    if not response:
        # Log the exception
        exception(
            exception=Exception("Failed to track mod"),
            message="Failed to track mod",
            name="nexus.track_mod",
        )

        # Return an empty dictionary if the response is not OK
        return {}

    # Check if the response is OK
    if response.get("reason") == "OK":
        # Return the tracked mod
        return response.get("body", {})
    else:
        # Log the exception
        exception(
            exception=Exception(response.get("reason")),
            message="Failed to track mod",
            name="nexus.track_mod",
        )

    # Return an empty dictionary if the response is not OK
    return {}


def untrack_mod(
    api_key: str,
    game: str,
    mod_id: int,
) -> Dict[str, Any]:
    """
    Performs an asynchronous GET request to the Nexus API
    to untrack a specific mod for a specific game.

    :param api_key: The API key to use for authentication.
    :type api_key: str
    :param game: The name of the game to untrack a mod for.
    :type game: str
    :param mod_id: The ID of the mod to untrack.
    :type mod_id: int

    :return: A dictionary containing information about the untracked mod.
    :rtype: Dict[str, Any]

    :raises Exception: If the response is not OK.
    """

    # Send a GET request to the Nexus Untrack Mod API
    response: Optional[Dict[str, Any]] = http_delete(
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "apikey": api_key,
        },
        params={
            "game": game,
            "mod_id": mod_id,
        },
        url="https://api.nexusmods.com/v1/users/tracked_mods.json",
    )

    # Check if the response exists
    if not response:
        # Log the exception
        exception(
            exception=Exception("Failed to untrack mod"),
            message="Failed to untrack mod",
            name="nexus.untrack_mod",
        )

        # Return an empty dictionary if the response is not OK
        return {}

    # Check if the response is OK
    if response.get("reason") == "OK":
        # Return the untracked mod
        return response.get("body", {})
    else:
        # Log the exception
        exception(
            exception=Exception(response.get("reason")),
            message="Failed to untrack mod",
            name="nexus.untrack_mod",
        )

    # Return an empty dictionary if the response is not OK
    return {}


def validate_api_key(api_key: str) -> Dict[str, Any]:
    """
    Performs an asynchronous GET request to the Nexus API
    to validate an API key.

    :param api_key: The API key to validate.
    :type api_key: str

    :return: A dictionary containing information about the validated API key.
    :rtype: Dict[str, Any]

    :raises Exception: If the response is not OK.
    """

    # Send a GET request to the Nexus Validate API Key API
    response: Optional[Dict[str, Any]] = http_get(
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "apikey": api_key,
        },
        url="https://api.nexusmods.com/v1/users/validate.json",
    )

    # Check if the response exists
    if not response:
        # Log the exception
        exception(
            exception=Exception("Failed to validate API key"),
            message="Failed to validate API key",
            name="nexus.validate_api_key",
        )

        # Return an empty dictionary if the response is not OK
        return {}

    # Check if the response is OK
    if response.get("reason") == "OK":
        # Return the validated API key
        return response.get("body", {})
    else:
        # Log the exception
        exception(
            exception=Exception(response.get("reason")),
            message="Failed to validate API key",
            name="nexus.validate_api_key",
        )

    # Return an empty dictionary if the response is not OK
    return {}
