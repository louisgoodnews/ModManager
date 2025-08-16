"""
Author: Louis Goodnews
Date: 2025-08-14
"""

import tkinter

from tkinter.constants import NSEW
from typing import Any, Callable, Final, List, Optional

from utils.constants import DEFAULT_FONT, DEFAULT_FONT_SIZE
from utils.dispatcher import dispatch
from utils.logging import exception, info


__all__: Final[List[str]] = [
    "add_edit_menu_command",
    "add_file_menu_command",
    "add_view_menu_command",
    "bottom_frame",
    "center_frame",
    "clear_center_frame",
    "edit_menu",
    "file_menu",
    "get_bottom_frame",
    "get_center_frame",
    "get_edit_menu",
    "get_file_menu",
    "get_main_ui",
    "get_main_window",
    "get_menu",
    "get_top_frame",
    "get_view_menu",
    "main_window",
    "menu",
    "top_frame",
    "view_menu",
]


BOTTOM_frame: Optional[tkinter.Frame] = None

CENTER_frame: Optional[tkinter.Frame] = None

EDIT_MENU: Optional[tkinter.Menu] = None

FILE_MENU: Optional[tkinter.Menu] = None

MAIN_WINDOW: Optional[tkinter.Tk] = None

MENU: Optional[tkinter.Menu] = None

TOP_frame: Optional[tkinter.Frame] = None

VIEW_MENU: Optional[tkinter.Menu] = None


def _configure_main_window_grid() -> None:
    """
    Configures the grid for the main window.

    :return: None
    :rtype: None
    """

    # Declare the global variable
    global MAIN_WINDOW

    # Assert that the main window exists
    assert MAIN_WINDOW is not None

    # Configure the 1st (left) column to weight 1
    MAIN_WINDOW.grid_columnconfigure(
        index=0,
        weight=1,
    )

    # Configure the 0th (top) row to weight 0
    MAIN_WINDOW.grid_rowconfigure(
        index=0,
        weight=0,
    )

    # Configure the 1st (top) row to weight 1
    MAIN_WINDOW.grid_rowconfigure(
        index=1,
        weight=1,
    )

    # Configure the 2nd (bottom) row to weight 0
    MAIN_WINDOW.grid_rowconfigure(
        index=2,
        weight=0,
    )


def _on_wm_delete(event: Optional[tkinter.Event] = None) -> None:
    """
    Closes the main window.

    :param event: The event that triggered the function. Defaults to None.
    :type event: Optional[tkinter.Event]

    :return: None
    :rtype: None
    """

    # Declare the global variable
    global MAIN_WINDOW, BOTTOM_frame, CENTER_frame, EDIT_MENU, FILE_MENU, MENU, TOP_frame, VIEW_MENU

    # Assert that the main window exists
    assert MAIN_WINDOW is not None

    # Unbind the WM_DELETE_WINDOW event
    MAIN_WINDOW.protocol(
        func=None,
        name="WM_DELETE_WINDOW",
    )

    # Attempt to dispatch the MOD_MANAGER_WINDOW_CLOSED event to the 'global' namespace
    try:
        # Dispatch the BROADCAST_APPLICATION_SHUTDOWN event into the 'global' namespace
        dispatch(
            event="BROADCAST_APPLICATION_SHUTDOWN",
            namespace="global",
        )

        # Dispatch the MOD_MANAGER_WINDOW_CLOSED event into the 'global' namespace
        dispatch(
            event="MOD_MANAGER_WINDOW_CLOSED",
            namespace="global",
        )
    except Exception as e:
        # Log the exception
        exception(
            exception=e,
            message="Failed to dispatch MOD_MANAGER_WINDOW_CLOSED event",
            name="gui.main_window._on_wm_delete",
        )

    # Log an info message
    info(
        message="Closing main window...",
        name="gui.main_window._on_wm_delete",
    )

    # Close the main window
    MAIN_WINDOW.destroy()

    # Set the main window to None
    MAIN_WINDOW = None

    # Set the bottom frame to None
    BOTTOM_frame = None

    # Set the center frame to None
    CENTER_frame = None

    # Set the edit menu to None
    EDIT_MENU = None

    # Set the file menu to None
    FILE_MENU = None

    # Set the menu to None
    MENU = None

    # Set the top frame to None
    TOP_frame = None

    # Set the view menu to None
    VIEW_MENU = None


def add_edit_menu_command(
    function: Callable[[Any], None],
    label: str,
    **kwargs: Any,
) -> None:
    """
    Adds the edit menu command to the menu.

    :param function: The function to add to the edit menu command.
    :type function: Callable[[Any], None]
    :param label: The label for the edit menu command.
    :type label: str
    :param kwargs: Additional keyword arguments to pass to the add_cascade method.
    :type kwargs: Any

    :return: None
    :rtype: None
    """

    # Declare the global variable
    global EDIT_MENU

    # Assert that the edit menu exists
    assert EDIT_MENU is not None

    # Add the edit menu command to the menu
    EDIT_MENU.add_command(
        command=function,
        font=(
            DEFAULT_FONT,
            DEFAULT_FONT_SIZE,
        ),
        label=label,
        **kwargs,
    )

    # Log an info message
    info(
        message=f"Added edit menu command: {label}",
        name="gui.main_window.add_edit_menu_command",
    )


def add_file_menu_command(
    function: Callable[[Any], None],
    label: str,
    **kwargs: Any,
) -> None:
    """
    Adds the file menu command to the menu.

    :param function: The function to add to the file menu command.
    :type function: Callable[[Any], None]
    :param label: The label for the file menu command.
    :type label: str
    :param kwargs: Additional keyword arguments to pass to the add_cascade method.
    :type kwargs: Any

    :return: None
    :rtype: None
    """

    # Declare the global variable
    global FILE_MENU

    # Assert that the file menu exists
    assert FILE_MENU is not None

    # Add the file menu command to the menu
    FILE_MENU.add_command(
        command=function,
        font=(
            DEFAULT_FONT,
            DEFAULT_FONT_SIZE,
        ),
        label=label,
        **kwargs,
    )

    # Log an info message
    info(
        message=f"Added file menu command: {label}",
        name="gui.main_window.add_file_menu_command",
    )


def add_view_menu_command(
    function: Callable[[Any], None],
    label: str,
    **kwargs: Any,
) -> None:
    """
    Adds the view menu command to the menu.

    :param function: The function to add to the view menu command.
    :type function: Callable[[Any], None]
    :param label: The label for the view menu command.
    :type label: str
    :param kwargs: Additional keyword arguments to pass to the add_cascade method.
    :type kwargs: Any

    :return: None
    :rtype: None
    """

    # Declare the global variable
    global VIEW_MENU

    # Assert that the view menu exists
    assert VIEW_MENU is not None

    # Add the view menu command to the menu
    VIEW_MENU.add_command(
        command=function,
        font=(
            DEFAULT_FONT,
            DEFAULT_FONT_SIZE,
        ),
        label=label,
        **kwargs,
    )

    # Log an info message
    info(
        message=f"Added view menu command: {label}",
        name="gui.main_window.add_view_menu_command",
    )


def bottom_frame() -> tkinter.Frame:
    """
    Returns the bottom Frame.

    :return: The bottom Frame.
    :rtype: tkinter.Frame
    """

    # Declare the global variable
    global BOTTOM_frame

    # Assert that the bottom Frame exists
    assert BOTTOM_frame is not None

    # Return the bottom Frame
    return BOTTOM_frame


def center_frame() -> tkinter.Frame:
    """
    Returns the center Frame.

    :return: The center Frame.
    :rtype: tkinter.Frame
    """

    # Declare the global variable
    global CENTER_frame

    # Assert that the center Frame exists
    assert CENTER_frame is not None

    # Return the center Frame
    return CENTER_frame


def clear_center_frame() -> None:
    """
    Clears the center Frame.

    :return: None
    :rtype: None
    """

    # Declare the global variable
    global CENTER_frame

    # Assert that the center Frame exists
    assert CENTER_frame is not None

    # Get the children of the center Frame
    children: List[tkinter.Widget] = CENTER_frame.winfo_children()

    # Iterate over the children
    for child in children:
        # Destroy the child
        child.destroy()

    # Log an info message
    info(
        message="Cleared center Frame.",
        name="gui.main_window.clear_center_frame",
    )


def edit_menu() -> tkinter.Menu:
    """
    Returns the edit menu.

    :return: The edit menu.
    :rtype: tkinter.Menu
    """

    # Declare the global variable
    global EDIT_MENU

    # Assert that the edit menu exists
    assert EDIT_MENU is not None

    # Return the edit menu
    return EDIT_MENU


def file_menu() -> tkinter.Menu:
    """
    Returns the file menu.

    :return: The file menu.
    :rtype: tkinter.Menu
    """

    # Declare the global variable
    global FILE_MENU

    # Assert that the file menu exists
    assert FILE_MENU is not None

    # Return the file menu
    return FILE_MENU


def get_bottom_frame() -> tkinter.Frame:
    """
    Creates and returns the bottom Frame.

    This method is a singleton pattern implementation, ensuring that only one
    instance of the bottom Frame is created.

    :return: The bottom Frame.
    :rtype: tkinter.Frame
    """

    # Declare the global variables
    global BOTTOM_frame
    global MAIN_WINDOW

    # Check if the main window exists
    if not MAIN_WINDOW:
        # Get the main window
        get_main_window()

    # Check if the bottom Frame exists
    if not BOTTOM_frame:
        # Create the bottom Frame
        BOTTOM_frame = tkinter.Frame(
            background="#6750A4",
            height=25,
            master=main_window(),
        )

        # Configure the grid for the bottom Frame
        BOTTOM_frame.grid_columnconfigure(
            index=0,
            weight=1,
        )

        # Configure the grid for the bottom Frame
        BOTTOM_frame.grid_rowconfigure(
            index=0,
            weight=1,
        )

        # Place the bottom Frame in the grid
        BOTTOM_frame.grid(
            column=0,
            row=2,
            sticky=NSEW,
        )

    # Return the bottom Frame
    return BOTTOM_frame


def get_center_frame() -> tkinter.Frame:
    """
    Creates and returns the center Frame.

    This method is a singleton pattern implementation, ensuring that only one
    instance of the center Frame is created.

    :return: The center Frame.
    :rtype: tkinter.Frame
    """

    # Declare the global variables
    global CENTER_frame
    global MAIN_WINDOW

    # Check if the main window exists
    if not MAIN_WINDOW:
        # Get the main window
        get_main_window()

    # Check if the center Frame exists
    if not CENTER_frame:
        # Create the center Frame
        CENTER_frame = tkinter.Frame(
            background="#6750A4",
            master=main_window(),
        )

        # Configure the grid for the center Frame
        CENTER_frame.grid_columnconfigure(
            index=0,
            weight=1,
        )

        # Configure the grid for the center Frame
        CENTER_frame.grid_rowconfigure(
            index=0,
            weight=1,
        )

        # Place the center Frame in the grid
        CENTER_frame.grid(
            column=0,
            row=1,
            sticky=NSEW,
        )

    # Return the center Frame
    return CENTER_frame


def get_edit_menu() -> tkinter.Menu:
    """
    Creates and returns the edit menu.

    This method is a singleton pattern implementation, ensuring that only one
    instance of the edit menu is created.

    :return: The edit menu.
    :rtype: tkinter.Menu
    """

    # Declare the global variable
    global EDIT_MENU

    # Check if the edit menu exists
    if not EDIT_MENU:
        # Create the edit menu
        EDIT_MENU = tkinter.Menu(
            background="#6750A4",
            font=(
                DEFAULT_FONT,
                DEFAULT_FONT_SIZE,
            ),
            foreground="white",
            master=menu(),
            name="edit",
        )

    # Assert that the edit menu exists
    assert EDIT_MENU is not None

    # Return the edit menu
    return EDIT_MENU


def get_file_menu() -> tkinter.Menu:
    """
    Creates and returns the file menu.

    This method is a singleton pattern implementation, ensuring that only one
    instance of the file menu is created.

    :return: The file menu.
    :rtype: tkinter.Menu
    """

    # Declare the global variable
    global FILE_MENU

    # Check if the file menu exists
    if not FILE_MENU:
        # Create the file menu
        FILE_MENU = tkinter.Menu(
            background="#6750A4",
            font=(
                DEFAULT_FONT,
                DEFAULT_FONT_SIZE,
            ),
            foreground="white",
            master=menu(),
            name="file",
        )

    # Assert that the file menu exists
    assert FILE_MENU is not None

    # Return the file menu
    return FILE_MENU


def get_main_ui() -> tkinter.Tk:
    """
    Creates and returns the main UI.

    This method is a singleton pattern implementation, ensuring that only one
    instance of the main UI is created.

    :return: The main UI.
    :rtype: tkinter.Tk
    """

    # Create the main window
    get_main_window()

    # Create the top Frame
    get_top_frame()

    # Create the menu
    get_menu()

    # Create the center Frame
    get_center_frame()

    # Create the bottom Frame
    get_bottom_frame()

    # Return the main window
    return main_window()


def get_main_window(
    title: str = "Mod Manager",
    width: int = 1920,
    height: int = 1080,
) -> tkinter.Tk:
    """
    Creates and returns the main window.

    This method is a singleton pattern implementation, ensuring that only one
    instance of the main window is created.

    :param title: The title of the main window. Defaults to "Mod Manager".
    :type title: str
    :param width: The width of the main window. Defaults to 1920.
    :type width: int
    :param height: The height of the main window. Defaults to 1080.
    :type height: int

    :return: The main window.
    :rtype: tkinter.Tk
    """

    # Declare the global variable
    global MAIN_WINDOW

    # Check if the main window exists
    if not MAIN_WINDOW:
        # Create the main window
        MAIN_WINDOW = tkinter.Tk()

        # Set the title of the main window
        MAIN_WINDOW.title(title)

        # Set the geometry of the main window
        MAIN_WINDOW.geometry(f"{width}x{height}")

        # Configure the grid for the main window
        _configure_main_window_grid()

        # Bind the WM_DELETE_WINDOW event to the _on_wm_delete function
        MAIN_WINDOW.protocol(
            func=_on_wm_delete,
            name="WM_DELETE_WINDOW",
        )

    # Assert that the main window exists
    assert MAIN_WINDOW is not None

    # Return the main window
    return MAIN_WINDOW


def get_menu() -> tkinter.Menu:
    """
    Creates and returns the menu.

    This method is a singleton pattern implementation, ensuring that only one
    instance of the menu is created.

    :return: The menu.
    :rtype: tkinter.Menu
    """

    # Declare the global variable
    global MENU

    # Check if the menu exists
    if not MENU:
        # Create the menu
        MENU = tkinter.Menu(
            background="#6750A4",
            font=(
                DEFAULT_FONT,
                DEFAULT_FONT_SIZE,
            ),
            foreground="white",
            master=main_window(),
        )

        MENU.add_cascade(
            label="File",
            menu=get_file_menu(),
        )

        MENU.add_cascade(
            label="Edit",
            menu=get_edit_menu(),
        )

        MENU.add_cascade(
            label="View",
            menu=get_view_menu(),
        )

        # Configure the menu for the main window
        main_window().config(menu=MENU)

    # Assert that the menu exists
    assert MENU is not None

    # Return the menu
    return MENU


def get_top_frame() -> tkinter.Frame:
    """
    Creates and returns the top Frame.

    This method is a singleton pattern implementation, ensuring that only one
    instance of the top Frame is created.

    :return: The top Frame.
    :rtype: tkinter.Frame
    """

    # Declare the global variables
    global TOP_frame
    global MAIN_WINDOW

    # Check if the main window exists
    if not MAIN_WINDOW:
        # Get the main window
        get_main_window()

    # Check if the top Frame exists
    if not TOP_frame:
        # Create the top Frame
        TOP_frame = tkinter.Frame(
            background="#6750A4",
            master=main_window(),
        )

        # Configure the grid for the top Frame
        TOP_frame.grid_columnconfigure(
            index=0,
            weight=1,
        )

        # Configure the grid for the top Frame
        TOP_frame.grid_rowconfigure(
            index=0,
            weight=1,
        )

        # Place the top Frame in the grid
        TOP_frame.grid(
            column=0,
            row=0,
            sticky=NSEW,
        )

    # Return the top Frame
    return TOP_frame


def get_view_menu() -> tkinter.Menu:
    """
    Creates and returns the view menu.

    This method is a singleton pattern implementation, ensuring that only one
    instance of the view menu is created.

    :return: The view menu.
    :rtype: tkinter.Menu
    """

    # Declare the global variable
    global VIEW_MENU

    # Check if the view menu exists
    if not VIEW_MENU:
        # Create the view menu
        VIEW_MENU = tkinter.Menu(
            background="#6750A4",
            font=(
                DEFAULT_FONT,
                DEFAULT_FONT_SIZE,
            ),
            foreground="white",
            master=menu(),
            name="view",
        )

    # Assert that the view menu exists
    assert VIEW_MENU is not None

    # Return the view menu
    return VIEW_MENU


def main_window() -> tkinter.Tk:
    """
    Returns the main window.

    :return: The main window.
    :rtype: tkinter.Tk
    """

    # Declare the global variable
    global MAIN_WINDOW

    # Assert that the main window exists
    assert MAIN_WINDOW is not None

    # Return the main window
    return MAIN_WINDOW


def menu() -> tkinter.Menu:
    """
    Returns the menu.

    :return: The menu.
    :rtype: tkinter.Menu
    """

    # Declare the global variable
    global MENU

    # Assert that the menu exists
    assert MENU is not None

    # Return the menu
    return MENU


def top_frame() -> tkinter.Frame:
    """
    Returns the top Frame.

    :return: The top Frame.
    :rtype: tkinter.Frame
    """

    # Declare the global variable
    global TOP_frame

    # Assert that the top Frame exists
    assert TOP_frame is not None

    # Return the top Frame
    return TOP_frame


def view_menu() -> tkinter.Menu:
    """
    Returns the view menu.

    :return: The view menu.
    :rtype: tkinter.Menu
    """

    # Declare the global variable
    global VIEW_MENU

    # Assert that the view menu exists
    assert VIEW_MENU is not None

    # Return the view menu
    return VIEW_MENU
