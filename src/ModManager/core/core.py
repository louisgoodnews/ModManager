"""
Author: Louis Goodnews
Date: 2025-09-01

A module containing the core functions used throughout the application.
"""

import tkinter

from datetime import datetime
from typing import Any, Dict, Final, List

from Dispatcher.core.core import DispatcherEvent

from utils.constants import APPLICATION_NAME, DISPATCHER, GLOBAL, LOGGER, VERSION
from utils.events import (
    BROADCAST_NOTIFICATION_APPLICATION_STARTED,
    BROADCAST_REQUEST_APPLICATION_STOP,
    BROADCAST_REQUEST_CONFIRM_APPLICATION_STOP,
)
from utils.utils import subscribe_to_events, unsubscribe_from_events

from ui.window import Window

from DateUtil import DateUtil
from Dispatcher import Dispatcher, DispatcherEventNotification
from Logger import Logger


__all__: Final[List[str]] = ["Application"]


class ApplicationStartError(Exception):
    """
    An exception raised when the application fails to start.
    """

    pass


class ApplicationStopError(Exception):
    """
    An exception raised when the application fails to stop.
    """

    pass


class Application:
    """
    A class representing the application.
    """

    def __init__(self) -> None:
        """
        Initialize the Application instance.

        Returns:
            None
        """

        # Initialize the instance's Dispatcher instance
        self._dispatcher: Final[Dispatcher] = DISPATCHER

        # Initialize the instance's function IDs list
        self._function_ids: Final[List[str]] = subscribe_to_events(
            subscriptions=self.get_subscriptions()
        )

        # Initialize the instance's running state
        self._is_running: bool = False

        # Initialize the instance's Logger instance
        self._logger: Final[Logger] = LOGGER

        # Initialize the instance's start time
        self._start: Final[datetime] = DateUtil.now()

        # Initialize the instance's Window instance
        self._window: Final[Window] = Window()

    @property
    def bottom_frame(self) -> tkinter.Frame:
        """
        Get the bottom frame of the window.

        Returns:
            tkinter.Frame: The bottom frame of the window.
        """

        # Return the bottom frame of the window
        return self._window.bottom_frame

    @property
    def center_frame(self) -> tkinter.Frame:
        """
        Get the center frame of the window.

        Returns:
            tkinter.Frame: The center frame of the window.
        """

        # Return the center frame of the window
        return self._window.center_frame

    def get_subscriptions(self) -> List[Dict[str, Any]]:
        """
        Get the subscriptions of the application.

        Returns:
            List[Dict[str, Any]]: The subscriptions of the application.
        """

        # Initialize the subscriptions list
        subscriptions: List[Dict[str, Any]] = [
            {
                "event": BROADCAST_REQUEST_APPLICATION_STOP,
                "function": self.on_request_application_stop,
                "namespace": GLOBAL,
                "persistent": True,
            }
        ]

        # Return the subscriptions list
        return subscriptions

    def on_request_application_stop(
        self,
        event: DispatcherEvent,
    ) -> None:
        """
        Handle the request to stop the application.

        Args:
            event (DispatcherEvent): The event to handle.

        Returns:
            None
        """

        try:
            # Dispatch the BROADCAST_REQUEST_CONFIRM_APPLICATION_STOP in the GLOBAL namespace
            notification: DispatcherEventNotification = self._dispatcher.dispatch(
                event=BROADCAST_REQUEST_CONFIRM_APPLICATION_STOP,
                namespace=GLOBAL,
            )

            # Check if the notification has errors
            if notification.has_errors():
                # Log an error
                self._logger.error(
                    message=f"Caught an error while attempting to stop {APPLICATION_NAME} (v. {VERSION})",
                )

                # Exit the application with errors
                raise SystemExit(1)

        except Exception as e:
            # Log an exception
            self._logger.exception(
                exception=e,
                message=f"Caught an exception while attempting to stop {APPLICATION_NAME} (v. {VERSION})",
            )

            # Exit the application with errors
            raise SystemExit(1)

    def start(self) -> None:
        """
        Start the application.

        Returns:
            None
        """

        # Log an info message
        self._logger.info(
            message=f"{APPLICATION_NAME} (v. {VERSION}) is starting",
        )

        try:
            # Dispatch the BROADCAST_NOTIFICATION_APPLICATION_STARTED in the GLOBAL namespace
            notification: DispatcherEventNotification = self._dispatcher.dispatch(
                event=BROADCAST_NOTIFICATION_APPLICATION_STARTED,
                namespace=GLOBAL,
            )

            # Check if the notification has errors
            if notification.has_errors():
                # Log an error
                self._logger.error(
                    message=f"Caught an error while attempting to start {APPLICATION_NAME} (v. {VERSION})",
                )

                # Exit the application with errors
                raise SystemExit(1)

            # Set the application's running state
            self._is_running = True

            # Log an info message
            self._logger.info(
                message=f"{APPLICATION_NAME} (v. {VERSION}) has been started",
            )

            # Log an info message
            self._logger.info(
                message=f"{APPLICATION_NAME} (v. {VERSION}) has been started at {DateUtil.now().strftime('%H:%M:%S')}",
            )

            # Start the window instance's mainloop
            self._window.mainloop()
        except ApplicationStartError as e:
            # Log an exception
            self._logger.exception(
                exception=e,
                message=f"Caught an exception while attempting to start {APPLICATION_NAME} (v. {VERSION})",
            )

            # Exit the application with errors
            raise SystemExit(1)

    def shutdown(self) -> None:
        """
        Shutdown the application.

        Returns:
            None
        """

        # Check if the application is running
        if not self._is_running:
            # Log an error
            self._logger.error(
                message=f"{APPLICATION_NAME} (v. {VERSION}) is not running",
            )

            # Exit the application with errors
            raise SystemExit(1)

        try:
            # Dispatch the BROADCAST_REQUEST_CONFIRM_APPLICATION_STOP in the GLOBAL namespace
            notification: DispatcherEventNotification = self._dispatcher.dispatch(
                event=BROADCAST_REQUEST_CONFIRM_APPLICATION_STOP,
                namespace=GLOBAL,
            )

            # Check if the notification has errors
            if notification.has_errors():
                # Log an error
                self._logger.error(
                    message=f"Caught an error while attempting to dispatch the BROADCAST_REQUEST_CONFIRM_APPLICATION_STOP in the GLOBAL namespace",
                )

                # Exit the application with errors
                raise SystemExit(1)

            # Log an info message
            self._logger.info(
                message=f"{APPLICATION_NAME} (v. {VERSION}) is shutting down",
            )

            # Set the application's running state
            self._is_running = False

            # Log an info message
            self._logger.info(
                message=f"{APPLICATION_NAME} (v. {VERSION}) has been shutdown"
            )

            # Log an info message
            self._logger.info(
                message=f"{APPLICATION_NAME} (v. {VERSION}) ran for {DateUtil.calculate_difference_in_seconds(start=self._start)} seconds",
            )

            # Unsubscribe from events
            unsubscribe_from_events(function_ids=self._function_ids)

            # Exit the application without errors
            raise SystemExit(0)
        except ApplicationStopError as e:
            # Log an exception
            self._logger.exception(
                exception=e,
                message=f"Caught an exception while attempting to shutdown {APPLICATION_NAME} (v. {VERSION})",
            )

            # Exit the application
            raise SystemExit(1)
