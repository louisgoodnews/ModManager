"""
Author: Louis Goodnews
Date: 2025-08-14
"""

import tkinter

from tkinter.constants import ALL, HORIZONTAL, NSEW, NW, VERTICAL
from typing import Final, List, Optional


__all__: Final[List[str]] = ["get_scrolled_frame"]


def get_scrolled_frame(
    master: tkinter.Widget,
    scroll_horizontal: bool = False,
    scroll_vertical: bool = True,
) -> tkinter.Frame:
    """
    Returns a scrolled frame.

    :param master: The master widget.
    :type master: tkinter.Widget
    :param scroll_horizontal: Whether to scroll horizontally.
    :type scroll_horizontal: bool
    :param scroll_vertical: Whether to scroll vertically.
    :type scroll_vertical: bool

    :return: The scrolled frame.
    :rtype: tkinter.Frame
    """

    def _on_canvas_configure(event: Optional[tkinter.Event] = None) -> None:
        """
        Configures the canvas.

        :param event: The event that triggered the function. Defaults to None.
        :type event: Optional[tkinter.Event]

        :return: None
        :rtype: None
        """

        # Configure the canvas
        canvas.configure(
            scrollregion=canvas.bbox(ALL),
        )

    def _on_canvas_scroll(
        event: tkinter.Event,
    ) -> None:
        """
        Scrolls the canvas.

        :param event: The event that triggered the function.
        :type event: tkinter.Event

        :return: None
        :rtype: None
        """

        # Scroll the canvas
        canvas.yview_scroll(
            event.delta,
            "units",
        )

    def _on_frame_configure(event: Optional[tkinter.Event] = None) -> None:
        """
        Configures the frame.

        :param event: The event that triggered the function. Defaults to None.
        :type event: Optional[tkinter.Event]

        :return: None
        :rtype: None
        """

        # Configure the canvas
        canvas.configure(
            scrollregion=canvas.bbox(ALL),
        )

    # Create the container
    container: tkinter.Frame = tkinter.Frame(
        master=master,
    )

    # Configure the grid for the container
    container.grid_columnconfigure(
        index=0,
        weight=1,
    )

    container.grid_rowconfigure(
        index=0,
        weight=1,
    )

    container.grid_rowconfigure(
        index=1,
        weight=0,
    )

    container.grid(
        column=0,
        row=0,
        sticky=NSEW,
    )

    # Create the canvas
    canvas: tkinter.Canvas = tkinter.Canvas(
        master=container,
    )

    if scroll_vertical:
        # Create the scrollbar
        vertical_scrollbar: tkinter.Scrollbar = tkinter.Scrollbar(
            master=container,
            orient=VERTICAL,
            command=canvas.yview,
        )

        # Configure the canvas
        canvas.configure(
            yscrollcommand=vertical_scrollbar.set,
        )

        # Pack the scrollbar
        vertical_scrollbar.grid(
            column=1,
            row=0,
            sticky=NSEW,
        )

        # Bind the canvas scroll event
        canvas.bind(
            func=_on_canvas_scroll,
            sequence="<MouseWheel>",
        )

    if scroll_horizontal:
        # Create the scrollbar
        horizontal_scrollbar: tkinter.Scrollbar = tkinter.Scrollbar(
            master=container,
            orient=HORIZONTAL,
            command=canvas.xview,
        )

        # Configure the canvas
        canvas.configure(
            xscrollcommand=horizontal_scrollbar.set,
        )

        # Pack the scrollbar
        horizontal_scrollbar.grid(
            column=0,
            row=1,
            sticky=NSEW,
        )

    # Pack the canvas
    canvas.grid(
        column=0,
        row=0,
        sticky=NSEW,
    )

    # Create the frame
    frame: tkinter.Frame = tkinter.Frame(
        master=canvas,
    )

    # Configure the canvas
    canvas.configure(
        scrollregion=canvas.bbox(ALL),
    )

    # Bind the canvas configure event
    canvas.bind(
        func=_on_canvas_configure,
        sequence="<Configure>",
    )

    # Bind the frame configure event
    frame.bind(
        func=_on_frame_configure,
        sequence="<Configure>",
    )

    # Add the frame to the canvas
    canvas.create_window(
        (0, 0),
        anchor=NW,
        window=frame,
    )

    # Return the frame
    return frame
