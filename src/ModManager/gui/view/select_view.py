"""
Author: Louis Goodnews
Date: 2025-08-14
"""

import tkinter

from pathlib import Path
from tkinter import filedialog
from typing import Final, List, Optional, Union

from gui.main_window import main_window

from utils.constants import HOME_PATH
from utils.logging import info, warn


__all__: Final[List[str]] = [
    "select_directory",
    "select_file",
]


def select_directory(
    initialdir: Path = HOME_PATH,
    title: str = "Select Directory",
) -> Optional[Path]:
    """
    Opens a file dialog to select a directory.

    :param initialdir: The initial directory to display.
    :type initialdir: Path
    :param title: The title of the file dialog.
    :type title: str

    :return: The selected directory.
    :rtype: Optional[Path]
    """

    # Get the main window
    window: Optional[tkinter.Tk] = main_window()

    # Check if the main window exists
    if not window:
        # Log an error message
        warn(
            message="Main window does not exist",
            name="select_view.select_directory",
        )

        # Return None early
        return None

    # Open the file dialog
    file_path: Optional[str] = filedialog.askdirectory(
        initialdir=initialdir,
        mustexist=True,
        parent=window,
        title=title,
    )

    # Log an info message
    info(
        message=f"Selected directory: '{file_path}'",
        name="select_view.select_directory",
    )

    # Return the file path
    return Path(file_path) if file_path else None


def select_file(
    file_types: Union[str, List[str]],
    initialdir: Path = HOME_PATH,
    title: str = "Select File",
) -> Optional[Path]:
    """
    Opens a file dialog to select a file.

    :param file_types: The file types to select. Either a single extension string ('zip')
                       or a list of extensions (['zip', 'rar']).
    :param initialdir: The initial directory to display.
    :param title: The title of the file dialog.

    :return: The selected file, or None if the user cancelled.
    """

    # Get the main window
    window: Optional[tkinter.Tk] = main_window()

    # Check if the main window exists
    if not window:
        # Log an error message
        warn(
            message="Main window does not exist",
            name="select_view.select_file",
        )

        # Return None early
        return None

    # Normalize file_types
    if isinstance(
        file_types,
        str,
    ):
        # Set the extensions
        extensions: str = f"*.{file_types.lower()}"

        # Set the label
        label: str = f"{file_types.upper()} files"
    elif isinstance(
        file_types,
        list,
    ):
        # Set the extensions
        extensions: str = " ".join(f"*.{ft.lower()}" for ft in file_types)

        # Set the label
        label: str = " / ".join(ft.upper() for ft in file_types) + " files"
    else:
        # Log an error message
        warn(
            message=f"Invalid file_types: {file_types}",
            name="select_view.select_file",
        )

        # Return None early
        return None

    # Open the file dialog
    file_path: Optional[str] = filedialog.askopenfilename(
        filetypes=[(label, extensions)],
        initialdir=initialdir,
        parent=window,
        title=title,
    )

    # Log an info message
    info(
        message=f"Selected file: '{file_path}'",
        name="select_view.select_file",
    )

    # Return the file path
    return Path(file_path) if file_path else None
