"""
Author: Louis Goodnews
Date: 2025-09-01
"""

import tkinter

from typing import Any, Dict, Final, List, Literal, Optional

from utils.constants import DEFAULT_GEOMETRY, DISPATCHER, GLOBAL, NSEW, WINDOW_NAME
from utils.events import (
    BROADCAST_NOTIFICATION_MAIN_WINDOW_DESTROY,
    BROADCAST_REQUEST_CONFIRM_APPLICATION_STOP,
)

from utils.utils import subscribe_to_events, unsubscribe_from_events

from Dispatcher import Dispatcher, DispatcherEvent, DispatcherEventNotification
from Logger import Logger


__all__: Final[List[str]] = ["Window"]


class Window(tkinter.Tk):
    """
    A class representing the main window.
    """

    def __init__(self) -> None:
        """
        Initialize the Window instance.

        Returns:
            None
        """

        # Initialize the instance's tkinter.Tk instance
        super().__init__()

        # Initialize the instance's Dispatcher instance
        self._dispatcher: Final[Dispatcher] = DISPATCHER

        # Initialize the instance's function IDs list
        self._function_ids: Final[List[str]] = subscribe_to_events(
            subscriptions=self.get_subscriptions()
        )

        # Initalize the instance's Logger instance
        self._logger: Final[Logger] = Logger.get_logger(name=self.__class__.__name__)

        # Set the geometry of the window
        self.geometry(newGeometry=DEFAULT_GEOMETRY)

        # Set the title of the window
        self.title(string=WINDOW_NAME)

        # Set the protocol for the WM_WINDOW_DESTROY event
        self.protocol(
            func=self.on_wm_window_destroy,
            name="WM_WINDOW_DESTROY",
        )

        # Configure the grid of the window
        self.configure_grid()

        # Create the widgets of the window
        self.create_widgets()

    @property
    def bottom_frame(self) -> tkinter.Frame:
        """
        Get the bottom frame of the window.

        Returns:
            tkinter.Frame: The bottom frame of the window.
        """

        return self._bottom_frame

    @property
    def center_frame(self) -> tkinter.Frame:
        """
        Get the center frame of the window.

        Returns:
            tkinter.Frame: The center frame of the window.
        """

        return self._center_frame

    @property
    def top_frame(self) -> tkinter.Frame:
        """
        Get the top frame of the window.

        Returns:
            tkinter.Frame: The top frame of the window.
        """

        return self._top_frame

    def clear(
        self,
        name: Literal[
            "bottom",
            "center",
            "top",
        ],
    ) -> None:
        """
        Clear the specified frame of the window.

        Args:
            name (Literal["bottom", "center", "top"]: The name of the frame to clear.

        Returns:
            None

        Raises:
            ValueError: If the name is invalid.
        """

        # Check if the name is valid
        if name not in ("bottom", "center", "top"):
            # Raise a ValueError
            self._logger.exception(
                exception=ValueError(f"Invalid frame name: {name}"),
                message=f"Caught an error while attempting to clear the {name} frame of the window",
            )

        # Clear the specified frame
        getattr(
            self,
            f"clear_{name}_frame",
        )()

    def clear_bottom_frame(self) -> None:
        """
        Clear the bottom frame of the window.

        Returns:
            None
        """

        # Iterate over the widgets of the bottom frame
        for widget in self._bottom_frame.winfo_children():
            # Destroy the widget
            widget.destroy()

    def clear_center_frame(self) -> None:
        """
        Clear the center frame of the window.

        Returns:
            None
        """

        # Iterate over the widgets of the center frame
        for widget in self._center_frame.winfo_children():
            # Destroy the widget
            widget.destroy()

    def clear_top_frame(self) -> None:
        """
        Clear the top frame of the window.

        Returns:
            None
        """

        # Iterate over the widgets of the top frame
        for widget in self._top_frame.winfo_children():
            # Destroy the widget
            widget.destroy()

    def configure_grid(self) -> None:
        """
        Configure the grid of the window.

        Returns:
            None
        """

        # Configure the grid of the window
        # Configure the 1st column of the grid to weigh 1
        self.grid_columnconfigure(
            index=0,
            weight=1,
        )

        # Configure the 1st row of the grid to weigh 1
        self.grid_rowconfigure(
            index=0,
            weight=1,
        )

        # Configure the 2nd row of the grid to weigh 1
        self.grid_rowconfigure(
            index=1,
            weight=1,
        )

        # Configure the 3rd row of the grid to weigh 0
        self.grid_rowconfigure(
            index=2,
            weight=0,
        )

    def create_widgets(self) -> None:
        """
        Create the widgets of the window.

        Returns:
            None
        """

        # Initialize the instance's 'top_frame' tkinter.Frame instance
        self._top_frame: tkinter.Frame = tkinter.Frame(self)

        # Grid the instance's 'top_frame' tkinter.Frame instance
        self._top_frame.grid(
            column=0,
            row=0,
            sticky=NSEW,
        )

        # Initialize the instance's 'center_frame' tkinter.Frame instance
        self._center_frame: tkinter.Frame = tkinter.Frame(self)

        # Grid the instance's 'center_frame' tkinter.Frame instance
        self._center_frame.grid(
            column=0,
            row=1,
            sticky=NSEW,
        )

        # Initialize the instance's 'bottom_frame' tkinter.Frame instance
        self._bottom_frame: tkinter.Frame = tkinter.Frame(self)

        # Grid the instance's 'bottom_frame' tkinter.Frame instance
        self._bottom_frame.grid(
            column=0,
            row=2,
            sticky=NSEW,
        )

    def get_subscriptions(self) -> List[Dict[str, Any]]:
        """
        Get the subscriptions of the window.

        Returns:
            List[Dict[str, Any]]: The subscriptions of the window.
        """

        # Initialize the subscriptions list
        subscriptions: List[Dict[str, Any]] = [
            {
                "event": BROADCAST_REQUEST_CONFIRM_APPLICATION_STOP,
                "function": self.on_request_confirm_application_stop,
                "namespace": GLOBAL,
                "persistent": True,
            }
        ]

        # Return the subscriptions list
        return subscriptions

    def on_request_confirm_application_stop(
        self,
        event: DispatcherEvent,
    ) -> bool:
        """
        Handle the request to confirm the stop of the application.

        Args:
            event (DispatcherEvent): The event to handle.

        Returns:
            bool: True if the window was destroyed successfully, False otherwise.
        """

        # Unsubscribe from events
        unsubscribe_from_events(function_ids=self._function_ids)

        # Destroy the window
        self.quit()

        # Return True
        return True

    def on_wm_window_destroy(
        self,
        event: Optional[tkinter.Event] = None,
    ) -> None:
        """
        Handle the window destroy event.

        Args:
            event (Optional[tkinter.Event]): The event to handle.

        Returns:
            None
        """

        # Unsubscribe from events
        unsubscribe_from_events(function_ids=self._function_ids)

        # Dispatch the BROADCAST_NOTIFICATION_MAIN_WINDOW_DESTROY in the GLOBAL namespace
        notification: DispatcherEventNotification = self._dispatcher.dispatch(
            event=BROADCAST_NOTIFICATION_MAIN_WINDOW_DESTROY,
            namespace=GLOBAL,
        )

        # Check if the notification has errors
        if notification.has_errors():
            # Log an error
            self._logger.error(
                message=f"Caught an error while attempting to dispatch the BROADCAST_NOTIFICATION_MAIN_WINDOW_DESTROY in the GLOBAL namespace",
            )
