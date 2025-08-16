"""
Author: Louis Goodnews
Date: 2025-08-14
"""

import tkinter

from pathlib import Path
from tkinter.constants import END, FLAT, NSEW, SINGLE
from typing import Any, Dict, Final, List, Optional, Union

from gui.main_window import center_frame, clear_center_frame, main_window
from gui.view.select_view import select_directory, select_file
from gui.widgets import get_scrolled_frame

from utils.constants import DEFAULT_FONT, DEFAULT_FONT_SIZE, DOWNLOAD_PATH
from utils.dispatcher import dispatch, register, unregister
from utils.logging import debug, exception, info
from utils.mod_installer import install_mod, uninstall_mod, update_mod


__all__: Final[List[str]] = ["get_mod_list_view"]


CURRENT_GAME: Optional[Dict[str, Any]] = None
REGISTRATION_IDS: Final[List[str]] = []
SCROLLED_FRAME: Optional[tkinter.Frame] = None


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


def _on_add_game_button_click() -> None:
    """
    Adds a game to the database.

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

        # Log an info message
        info(
            message=f"Selected game: '{path.name}'",
            name="mod_list_view._on_game_select_button_click",
        )

        # Dispatch the SELECT_GAME event
        CURRENT_GAME = dispatch(
            event="REQUEST_INSERT_GAME",
            name=path.name,
            namespace="global",
            path=path,
        ).get("_on_request_insert_game", {})

        info(
            message=f"Changed selected game to: '{CURRENT_GAME}'",
            name="mod_list_view._on_game_select_button_click",
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
    global CURRENT_GAME, SCROLLED_FRAME

    # Attempt to dispatch the REQUEST_GET_ALL_GAMES event
    games: List[Dict[str, Any]] = dispatch(
        event="REQUEST_GET_ALL_GAMES",
        namespace="global",
    ).get("_on_request_get_all_games", [])

    # Check if the games list is empty
    if not games:
        # Log an info message
        info(
            message="No games found",
            name="mod_list_view._on_game_select_button_click",
        )

        # Return early
        return

    def _on_listbox_select(event: Optional[tkinter.Event] = None) -> None:
        """
        Selects the game.

        :param event: The event that triggered the function. Defaults to None.
        :type event: Optional[tkinter.Event]

        :return: None
        :rtype: None
        """

        # Declare the global variable
        global CURRENT_GAME

        # Check if the event is None
        if not event:
            # Return early
            return

        listbox: tkinter.Listbox = event.widget

        # Get the selected game
        selected_game: str = listbox.get(
            first=listbox.curselection()[0],
        )

        # Set the current game
        game: Dict[str, Any] = next(
            (game for game in games if game.get("name") == selected_game),
            None,
        )

        # Check if the game is None
        if not game:
            # Log an info message
            info(
                message="Game not found",
                name="mod_list_view._on_game_select_button_click",
            )

            # Return early
            return

        # Set the current game
        CURRENT_GAME = game

        # Log an info message
        info(
            message=f"Selected game: '{CURRENT_GAME}'",
            name="mod_list_view._on_game_select_button_click",
        )

        # Attempt to dispatch the REQUEST_GET_MODS_FOR_GAME event
        mods_for_game: List[Dict[str, Any]] = dispatch(
            event="REQUEST_GET_MODS_FOR_GAME",
            game_id=CURRENT_GAME.get("id"),
            namespace="global",
        ).get("_on_request_get_mods_for_game", [])

        # Clear the scrolled frame
        clear_scrolled_frame()

        # Iterate over the mods for the game
        for mod_for_game in mods_for_game:
            # Get the mod list view item
            get_mod_list_view_item(
                master=SCROLLED_FRAME,
                name=mod_for_game.get("name"),
            )

        # Destroy the toplevel
        toplevel.destroy()

    # Create the toplevel
    toplevel: tkinter.Toplevel = tkinter.Toplevel(master=main_window())

    # Set the toplevel's title
    toplevel.title("Select Game")

    # Set the toplevel's geometry
    toplevel.geometry("400x400")

    # Configure the toplevel's 0th column to weight 1
    toplevel.grid_columnconfigure(
        index=0,
        weight=1,
    )

    # Configure the toplevel's 0th row to weight 1
    toplevel.grid_rowconfigure(
        index=0,
        weight=1,
    )

    # Create the listbox
    listbox: tkinter.Listbox = tkinter.Listbox(
        font=(
            DEFAULT_FONT,
            DEFAULT_FONT_SIZE,
        ),
        master=toplevel,
        selectmode=SINGLE,
    )

    # Grid the listbox
    listbox.grid(
        column=0,
        row=0,
        sticky=NSEW,
    )

    # Insert the game names into the listbox
    for game in games:
        # Insert the game name into the listbox
        listbox.insert(
            END,
            game.get("name"),
        )

    # Bind the listbox select event
    listbox.bind(
        func=_on_listbox_select,
        sequence="<<ListboxSelect>>",
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

    # Declare the global variable
    global CURRENT_GAME

    # Attempt to dispatch the INSTALL_MOD event
    try:
        # Dispatch the INSTALL_MOD event
        mods: List[Dict[str, Any]] = dispatch(
            event="REQUEST_SEARCH_MODS",
            game_code=CURRENT_GAME.get("code"),
            name=name,
            namespace="global",
        ).get("_on_request_search_mods", [])

        # Check if the mods list is empty
        if not mods:
            # Log an info message
            info(
                message="No mods found",
                name="mod_list_view._on_install_click",
            )

            # Return early
            return

        mod: Optional[Dict[str, Any]] = next(
            (mod for mod in mods if mod.get("name") == name),
            None,
        )

        # Check if the mod is None
        if not mod:
            # Log an info message
            info(
                message="Mod not found",
                name="mod_list_view._on_install_click",
            )

            # Return early
            return

        mod["symlink_target"] = select_directory(
            initialdir=Path(CURRENT_GAME.get("path", "")),
            title="Select Symlink Target",
        )

        # Install the mod
        install_mod(mod=mod)
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

    # Declare the global variable
    global CURRENT_GAME, SCROLLED_FRAME

    # Check if the game is None
    if not CURRENT_GAME:
        # Log an info message
        info(
            message="No game selected",
            name="mod_list_view._on_mod_select_button_click",
        )

        # Return early
        return

    # Attempt to dispatch the SELECT_GAME event
    try:
        # Select the game directory
        path: Optional[Path] = select_file(
            file_types=["7z", "rar", "zip"],
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
        mod: Optional[Dict[str, Any]] = dispatch(
            event="REQUEST_INSERT_MOD",
            game_code=CURRENT_GAME.get("code"),
            game_id=CURRENT_GAME.get("id"),
            name=path.name,
            namespace="global",
            path=path,
        ).get("_on_request_insert_mod", None)

        # Check if the mod is None
        if not mod:
            # Log an info message
            info(
                message="Mod not inserted",
                name="mod_list_view._on_mod_select_button_click",
            )

            # Return early
            return

        # Get the mod list view item
        get_mod_list_view_item(
            master=SCROLLED_FRAME,
            name=mod.get("name"),
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
        mods: List[Dict[str, Any]] = dispatch(
            event="REQUEST_SEARCH_MODS",
            game_code=CURRENT_GAME.get("code"),
            name=name,
            namespace="global",
        ).get("_on_request_search_mods", [])

        # Check if the mods list is empty
        if not mods:
            # Log an info message
            info(
                message="No mods found",
                name="mod_list_view._on_uninstall_click",
            )

            # Return early
            return

        mod: Optional[Dict[str, Any]] = next(
            (mod for mod in mods if mod.get("name") == name),
            None,
        )

        # Check if the mod is None
        if not mod:
            # Log an info message
            info(
                message="Mod not found",
                name="mod_list_view._on_uninstall_click",
            )

            # Return early
            return

        # Uninstall the mod
        uninstall_mod(mod=mod)
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
        # Dispatch the REQUEST_SEARCH_MODS event
        mods: List[Dict[str, Any]] = dispatch(
            event="REQUEST_SEARCH_MODS",
            game_code=CURRENT_GAME.get("code"),
            name=name,
            namespace="global",
        ).get("_on_request_search_mods", [])

        # Check if the mods list is empty
        if not mods:
            # Log an info message
            info(
                message="No mods found",
                name="mod_list_view._on_update_click",
            )

            # Return early
            return

        mod: Optional[Dict[str, Any]] = next(
            (mod for mod in mods if mod.get("name") == name),
            None,
        )

        # Check if the mod is None
        if not mod:
            # Log an info message
            info(
                message="Mod not found",
                name="mod_list_view._on_update_click",
            )

            # Return early
            return

        # Update the mod
        update_mod(mod=mod)
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


def clear_scrolled_frame() -> None:
    """
    Clears the scrolled frame.

    :return: None
    :rtype: None
    """

    # Iterate over the widgets in the scrolled frame
    for widget in scrolled_frame().winfo_children():
        # Destroy the widget
        widget.destroy()


def get_mod_list_view() -> None:
    """
    Returns the mod list view.

    :return: None
    :rtype: None
    """

    # Declare the global variable
    global SCROLLED_FRAME

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
        background="#6750A4",
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
        background="#6750A4",
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

    top_frame.grid_columnconfigure(
        index=3,
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
        background="#6750A4",
        command=_on_game_select_button_click,
        font=(
            DEFAULT_FONT,
            DEFAULT_FONT_SIZE,
        ),
        foreground="white",
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

    add_game_button: tkinter.Button = tkinter.Button(
        background="#6750A4",
        command=_on_add_game_button_click,
        font=(
            DEFAULT_FONT,
            DEFAULT_FONT_SIZE,
        ),
        foreground="white",
        master=top_frame,
        relief=FLAT,
        text="Add New Game",
    )

    add_game_button.grid(
        column=2,
        padx=5,
        pady=5,
        row=0,
    )

    mod_select_button: tkinter.Button = tkinter.Button(
        background="#6750A4",
        command=_on_mod_select_button_click,
        font=(
            DEFAULT_FONT,
            DEFAULT_FONT_SIZE,
        ),
        foreground="white",
        master=top_frame,
        relief=FLAT,
        text="Select Mod",
    )

    mod_select_button.grid(
        column=3,
        padx=5,
        pady=5,
        row=0,
    )

    # Create the bottom frame
    bottom_frame: tkinter.Frame = tkinter.Frame(
        background="#6750A4",
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
    SCROLLED_FRAME = get_scrolled_frame(
        master=bottom_frame,
    )

    SCROLLED_FRAME.configure(background="#6750A4")

    SCROLLED_FRAME.grid(
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

    # Configure the grid for the master frame
    master.grid_columnconfigure(
        index=len(master.winfo_children()),
        weight=1,
    )

    # Configure the grid for the master frame
    master.grid_rowconfigure(
        index=len(master.winfo_children()),
        weight=0,
    )

    # Create the frame
    frame: tkinter.Frame = tkinter.Frame(
        background="#6750A4",
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
        background="#6750A4",
        font=(DEFAULT_FONT, DEFAULT_FONT_SIZE),
        foreground="white",
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
        background="#6750A4",
        foreground="white",
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
        background="#6750A4",
        foreground="white",
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


def scrolled_frame() -> tkinter.Frame:
    """
    Returns the scrolled frame.

    :return: The scrolled frame.
    :rtype: tkinter.Frame
    """

    # Declare the global variable
    global SCROLLED_FRAME

    # Assert that the scrolled frame exists
    assert SCROLLED_FRAME is not None

    # Return the scrolled frame
    return SCROLLED_FRAME


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
