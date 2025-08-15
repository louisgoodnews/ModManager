"""
Author: Louis Goodnews
Date: 2025-08-15
"""

import tkinter

from datetime import datetime
from typing import Final, List

from utils.dispatcher import dispatch
from gui.main_window import get_main_ui
from gui.view.mod_list_view import get_mod_list_view


__all__: Final[List[str]] = [
    "register_subscriptions",
    "unregister_subscriptions",
]


START_TIME: Final[datetime] = datetime.now()


def create_tables() -> None:
    """
    Creates the tables.

    :return: None
    :rtype: None
    """

    # Import the functions locally
    from utils.database.games import create_games_table
    from utils.database.mods import create_mods_table

    # Create the games table
    create_games_table()

    # Create the mods table
    create_mods_table()


def register_database_service_subscriptions() -> None:
    """
    Registers the database service subscriptions.

    :return: None
    :rtype: None
    """

    # Import the function locally
    from utils.database.service import subscribe_to_events

    # Subscribe to events
    subscribe_to_events()


def register_subscriptions() -> None:
    """
    Registers the subscriptions.

    :return: None
    :rtype: None
    """

    # Register the database service subscriptions
    register_database_service_subscriptions()


def start_application() -> None:
    """
    Starts the ModManager application.

    This method is the entry point of the application.

    :return: None
    :rtype: None
    """

    # Get the main UI
    window: tkinter.Tk = get_main_ui()

    # Create the tables
    create_tables()

    # Register the subscriptions
    register_subscriptions()

    # Get the mod list view
    get_mod_list_view()

    # Dispatch the BROADCAST_APPLICATION_STARTUP event to the 'global' namespace
    dispatch(
        event="BROADCAST_APPLICATION_STARTUP",
        namespace="global",
    )

    # Run the main loop
    window.mainloop()


def unregister_subscriptions() -> None:
    """
    Unregisters the subscriptions.

    :return: None
    :rtype: None
    """

    # Unregister the database service subscriptions
    unregister_database_service_subscriptions()


def unregister_database_service_subscriptions() -> None:
    """
    Unregisters the database service subscriptions.

    :return: None
    :rtype: None
    """

    # Import the function locally
    from utils.database.service import unsubscribe_from_events

    # Unsubscribe from events
    unsubscribe_from_events()
