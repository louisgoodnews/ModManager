"""
Author: Louis Goodnews
Date: 2025-08-14
"""

import tkinter

from pathlib import Path
from tkinter.constants import FLAT, NSEW
from typing import Any, Dict, Final, List, Optional, Union

from gui.main_window import center_frame, clear_center_frame
from gui.view.select_view import select_directory, select_file
from gui.widgets import get_scrolled_frame

from utils.constants import DEFAULT_FONT, DEFAULT_FONT_SIZE, DOWNLOAD_PATH
from utils.dispatcher import dispatch, register, unregister
from utils.logging import exception, info


__all__: Final[List[str]] = ["get_mod_list_view"]


CURRENT_GAME: Optional[str] = None
REGISTRATION_IDS: Final[List[str]] = []


def _on_activate_click(
    name: str,
    event: Optional[tkinter.Event] = None,
) -> None:
    """
    Activates the mod list view item.

    :param event: The event that triggered the function. Defaults to None.
    :type event: Optional[tkinter.Event]
    :param name: The name of the mod list view item. Defaults to "".
    :type name: str

    :return: None
    :rtype: None
    """

    # Attempt to dispatch the ACTIVATE_MOD event
    try:
        # Dispatch the ACTIVATE_MOD event
        dispatch(
            event="ACTIVATE_MOD",
            name=name,
            namespace="core",
        )
    except Exception as e:
        # Log an exception
        exception(
            exception=e,
            message=f"Failed to activate mod list view item: '{name}'",
            name="mod_list_view._on_activate_click",
        )

        # Return early
        return

    # Log an info message
    info(
        message=f"Activated mod list view item: '{name}'",
        name="mod_list_view._on_activate_click",
    )


def _on_deactivate_click(
    name: str,
    event: Optional[tkinter.Event] = None,
) -> None:
    """
    Deactivates the mod list view item.

    :param event: The event that triggered the function. Defaults to None.
    :type event: Optional[tkinter.Event]
    :param name: The name of the mod list view item. Defaults to "".
    :type name: str

    :return: None
    :rtype: None
    """

    # Attempt to dispatch the DEACTIVATE_MOD event
    try:
        # Dispatch the DEACTIVATE_MOD event
        dispatch(
            event="DEACTIVATE_MOD",
            name=name,
            namespace="core",
        )
    except Exception as e:
        # Log an exception
        exception(
            exception=e,
            message=f"Failed to deactivate mod list view item: '{name}'",
            name="mod_list_view._on_deactivate_click",
        )

        # Return early
        return

    # Log an info message
    info(
        message=f"Deactivated mod list view item: '{name}'",
        name="mod_list_view._on_deactivate_click",
    )


def _on_delete_click(
    name: str,
    event: Optional[tkinter.Event] = None,
) -> None:
    """
    Deletes the mod list view item.

    :param event: The event that triggered the function. Defaults to None.
    :type event: Optional[tkinter.Event]
    :param name: The name of the mod list view item. Defaults to "".
    :type name: str

    :return: None
    :rtype: None
    """

    # Attempt to dispatch the DELETE_MOD event
    try:
        # Dispatch the DELETE_MOD event
        dispatch(
            event="DELETE_MOD",
            name=name,
            namespace="core",
        )
    except Exception as e:
        # Log an exception
        exception(
            exception=e,
            message=f"Failed to delete mod list view item: '{name}'",
            name="mod_list_view._on_delete_click",
        )

        # Return early
        return

    # Log an info message
    info(
        message=f"Deleted mod list view item: '{name}'",
        name="mod_list_view._on_delete_click",
    )


def _on_game_select_button_click() -> None:
    """
    Selects the game.

    :return: None
    :rtype: None
    """

    # Declare the global variable
    global CURRENT_GAME

    # Attempt to dispatch the SELECT_GAME event
    try:
        # Select the game directory
        path: Optional[Path] = select_directory(
            title="Select Game Directory",
        )

        # Check if the path exists
        if not path:
            # Log an info message
            info(
                message="Game directory not selected",
                name="mod_list_view._on_game_select_button_click",
            )

            # Return early
            return

        # Set the current game
        CURRENT_GAME = path.name

        # Log an info message
        info(
            message=f"Selected game: '{CURRENT_GAME}'",
            name="mod_list_view._on_game_select_button_click",
        )

        # Dispatch the SELECT_GAME event
        dispatch(
            event="SELECTED_GAME_DIRECTORY",
            name=path.name,
            namespace="core",
            path=path,
        )
    except Exception as e:
        # Log an exception
        exception(
            exception=e,
            message="Failed to select game",
            name="mod_list_view._on_game_select_button_click",
        )

        # Return early
        return

    # Log an info message
    info(
        message="Selected game",
        name="mod_list_view._on_game_select_button_click",
    )


def _on_install_click(
    name: str,
    event: Optional[tkinter.Event] = None,
) -> None:
    """
    Installs the mod list view item.

    :param event: The event that triggered the function. Defaults to None.
    :type event: Optional[tkinter.Event]
    :param name: The name of the mod list view item. Defaults to "".
    :type name: str

    :return: None
    :rtype: None
    """

    # Attempt to dispatch the INSTALL_MOD event
    try:
        # Dispatch the INSTALL_MOD event
        dispatch(
            event="INSTALL_MOD",
            name=name,
            namespace="core",
        )
    except Exception as e:
        # Log an exception
        exception(
            exception=e,
            message=f"Failed to install mod list view item: '{name}'",
            name="mod_list_view._on_install_click",
        )

        # Return early
        return

    # Log an info message
    info(
        message=f"Installed mod list view item: '{name}'",
        name="mod_list_view._on_install_click",
    )


def _on_mod_select_button_click() -> None:
    """
    Selects the mod list view item.

    :return: None
    :rtype: None
    """

    # Attempt to dispatch the SELECT_GAME event
    try:
        # Select the game directory
        path: Optional[Path] = select_file(
            file_types=["7zip", "rar", "zip"],
            initialdir=DOWNLOAD_PATH,
            title="Select Mod Directory",
        )

        # Check if the path exists
        if not path:
            # Log an info message
            info(
                message="Mod directory not selected",
                name="mod_list_view._on_mod_select_button_click",
            )

            # Return early
            return

        # Dispatch the SELECT_GAME event
        dispatch(
            event="SELECTED_MOD_DIRECTORY",
            name=path.name,
            namespace="core",
            path=path,
        )
    except Exception as e:
        # Log an exception
        exception(
            exception=e,
            message="Failed to select mod directory",
            name="mod_list_view._on_mod_select_button_click",
        )

        # Return early
        return

    # Log an info message
    info(
        message="Selected mod directory",
        name="mod_list_view._on_mod_select_button_click",
    )


def _on_uninstall_click(
    name: str,
    event: Optional[tkinter.Event] = None,
) -> None:
    """
    Uninstalls the mod list view item.

    :param event: The event that triggered the function. Defaults to None.
    :type event: Optional[tkinter.Event]
    :param name: The name of the mod list view item. Defaults to "".
    :type name: str

    :return: None
    :rtype: None
    """

    # Attempt to dispatch the UNINSTALL_MOD event
    try:
        # Dispatch the UNINSTALL_MOD event
        dispatch(
            event="UNINSTALL_MOD",
            name=name,
            namespace="core",
        )
    except Exception as e:
        # Log an exception
        exception(
            exception=e,
            message=f"Failed to uninstall mod list view item: '{name}'",
            name="mod_list_view._on_uninstall_click",
        )

        # Return early
        return

    # Log an info message
    info(
        message=f"Uninstalled mod list view item: '{name}'",
        name="mod_list_view._on_uninstall_click",
    )


def _on_update_click(
    name: str,
    event: Optional[tkinter.Event] = None,
) -> None:
    """
    Updates the mod list view item.

    :param event: The event that triggered the function. Defaults to None.
    :type event: Optional[tkinter.Event]
    :param name: The name of the mod list view item. Defaults to "".
    :type name: str

    :return: None
    :rtype: None
    """

    # Attempt to dispatch the UPDATE_MOD event
    try:
        # Dispatch the UPDATE_MOD event
        dispatch(
            event="UPDATE_MOD",
            name=name,
            namespace="core",
        )
    except Exception as e:
        # Log an exception
        exception(
            exception=e,
            message=f"Failed to update mod list view item: '{name}'",
            name="mod_list_view._on_update_click",
        )

        # Return early
        return

    # Log an info message
    info(
        message=f"Updated mod list view item: '{name}'",
        name="mod_list_view._on_update_click",
    )


def get_mod_list_view() -> None:
    """
    Returns the mod list view.

    :return: None
    :rtype: None
    """

    # Declare the master frame
    master: Optional[tkinter.Frame] = center_frame()

    # Check if the master frame exists
    if not master:
        # Log an error message
        exception(
            exception=Exception("Master frame does not exist"),
            message="Master frame does not exist",
            name="mod_list_view.get_mod_list_view",
        )

        # Return early
        return

    # Clear the center frame
    clear_center_frame()

    # Create the frame
    frame: tkinter.Frame = tkinter.Frame(
        master=master,
    )

    frame.grid_columnconfigure(
        index=0,
        weight=1,
    )

    frame.grid_rowconfigure(
        index=0,
        weight=0,
    )

    frame.grid_rowconfigure(
        index=1,
        weight=1,
    )

    frame.grid(
        column=0,
        row=0,
        sticky=NSEW,
    )

    # Create the top frame
    top_frame: tkinter.Frame = tkinter.Frame(
        master=frame,
    )

    top_frame.grid_columnconfigure(
        index=0,
        weight=1,
    )

    top_frame.grid_columnconfigure(
        index=1,
        weight=0,
    )

    top_frame.grid_columnconfigure(
        index=2,
        weight=0,
    )

    top_frame.grid_rowconfigure(
        index=0,
        weight=1,
    )

    top_frame.grid(
        column=0,
        row=0,
        sticky=NSEW,
    )

    game_select_button: tkinter.Button = tkinter.Button(
        command=_on_game_select_button_click,
        font=(
            DEFAULT_FONT,
            DEFAULT_FONT_SIZE,
        ),
        master=top_frame,
        relief=FLAT,
        text="Select Game",
    )

    game_select_button.grid(
        column=1,
        padx=5,
        pady=5,
        row=0,
    )

    mod_select_button: tkinter.Button = tkinter.Button(
        command=_on_mod_select_button_click,
        font=(
            DEFAULT_FONT,
            DEFAULT_FONT_SIZE,
        ),
        master=top_frame,
        relief=FLAT,
        text="Select Mod",
    )

    mod_select_button.grid(
        column=2,
        padx=5,
        pady=5,
        row=0,
    )

    # Create the bottom frame
    bottom_frame: tkinter.Frame = tkinter.Frame(
        master=frame,
    )

    bottom_frame.grid_columnconfigure(
        index=0,
        weight=1,
    )

    bottom_frame.grid_rowconfigure(
        index=0,
        weight=1,
    )

    bottom_frame.grid(
        column=0,
        row=1,
        sticky=NSEW,
    )

    # Create the scrolled frame
    scrolled_frame: tkinter.Frame = get_scrolled_frame(
        master=bottom_frame,
    )

    scrolled_frame.grid(
        column=0,
        row=0,
        sticky=NSEW,
    )

    # Subscribe to events
    subscribe_to_events()

    # Log an info message
    info(
        message="Loaded 'Mod List' view",
        name="mod_list_view.get_mod_list_view",
    )


def get_mod_list_view_item(
    master: tkinter.Frame,
    name: str,
) -> tkinter.Frame:
    """
    Returns the mod list view item.

    :param master: The master frame.
    :type master: tkinter.Frame
    :param name: The name of the mod list view item.
    :type name: str

    :return: The mod list view item.
    :rtype: tkinter.Frame
    """

    # Create the frame
    frame: tkinter.Frame = tkinter.Frame(
        master=master,
    )

    # Configure the grid for the frame
    frame.grid_columnconfigure(
        index=0,
        weight=1,
    )

    # Configure the grid for the frame
    frame.grid_columnconfigure(
        index=1,
        weight=0,
    )

    # Configure the grid for the frame
    frame.grid_rowconfigure(
        index=0,
        weight=1,
    )

    # Place the frame in the grid
    frame.grid(
        column=0,
        row=len(master.winfo_children()),
        sticky=NSEW,
    )

    # Create the label
    label: tkinter.Label = tkinter.Label(
        font=(DEFAULT_FONT, DEFAULT_FONT_SIZE),
        master=frame,
        text=name,
    )

    # Place the label in the grid
    label.grid(
        column=0,
        padx=5,
        pady=5,
        row=0,
        sticky=NSEW,
    )

    # Create the menu button
    menu_button: tkinter.Menubutton = tkinter.Menubutton(
        master=frame,
        text="...",
    )

    # Place the menu button in the grid
    menu_button.grid(
        column=1,
        padx=5,
        pady=5,
        row=0,
    )

    # Create the menu
    menu: tkinter.Menu = tkinter.Menu(
        master=menu_button,
    )

    # Configure the menu button
    menu_button.configure(
        menu=menu,
    )

    # Add the menu commands
    menu.add_command(
        command=lambda: _on_activate_click(name=name),
        label="Activate",
    )

    menu.add_command(
        command=lambda: _on_deactivate_click(name=name),
        label="Deactivate",
    )

    menu.add_command(
        command=lambda: _on_delete_click(name=name),
        label="Delete",
    )

    menu.add_command(
        command=lambda: _on_install_click(name=name),
        label="Install",
    )

    menu.add_command(
        command=lambda: _on_update_click(name=name),
        label="Update",
    )

    menu.add_command(
        command=lambda: _on_uninstall_click(name=name),
        label="Uninstall",
    )

    # Return the frame
    return frame


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
                "event": "UNREGISTER_MOD_LIST_VIEW",
                "function": on_unregister_mod_list_view,
                "namespace": "global",
                "persistent": False,
            },
        ]
    )

    # Return the subscriptions
    return subscriptions


def on_unregister_mod_list_view(event: Optional[str] = None) -> None:
    """
    Unsubscribes from events.

    :param event: The event that triggered the function. Defaults to None.
    :type event: Optional[str]

    :return: None
    :rtype: None
    """

    # Unsubscribe from events
    unsubscribe_from_events()


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
                False,
            ),
        )

        if not registration_id:
            # Log an error message
            exception(
                exception=Exception("Failed to register subscription"),
                message=f"Failed to register subscription: {subscription}",
                name="gui.view.mod_list_view.subscribe_to_events",
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
