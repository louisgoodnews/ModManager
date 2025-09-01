"""
Author: Louis Goodnews
Date: 2025-09-01

A module containing events used throughout the application.
"""

from typing import Final, List

from Dispatcher import DispatcherEvent, DispatcherEventFactory

__all__: Final[List[str]] = [
    "BROADCAST_NOTIFICATION_APPLICATION_STARTED",
    "BROADCAST_NOTIFICATION_MAIN_WINDOW_DESTROY",
    "BROADCAST_REQUEST_APPLICATION_STOP",
    "BROADCAST_REQUEST_CONFIRM_APPLICATION_STOP",
    "BROADCAST_REQUEST_CONFIRM_MAIN_WINDOW_DESTROY",
    "BROADCAST_REQUEST_UI_NAVIGATE_BACKWARD",
    "BROADCAST_REQUEST_UI_NAVIGATE_FORWARD",
]


# An event that represents a broadcasted notification that the application has started
BROADCAST_NOTIFICATION_APPLICATION_STARTED: Final[DispatcherEvent] = (
    DispatcherEventFactory.create_dispatcher_event(
        name="broadcast_notification_application_started"
    )
)

# An event that represents a broadcasted notification that the main window has been destroyed
BROADCAST_NOTIFICATION_MAIN_WINDOW_DESTROY: Final[DispatcherEvent] = (
    DispatcherEventFactory.create_dispatcher_event(
        name="broadcast_notification_main_window_destroy"
    )
)

# An event that represents a broadcasted request to stop the application
BROADCAST_REQUEST_APPLICATION_STOP: Final[DispatcherEvent] = (
    DispatcherEventFactory.create_dispatcher_event(
        name="broadcast_request_application_stop"
    )
)

# An event that represents a broadcasted request to confirm the stop of the application
BROADCAST_REQUEST_CONFIRM_APPLICATION_STOP: Final[DispatcherEvent] = (
    DispatcherEventFactory.create_dispatcher_event(
        name="broadcast_request_confirm_application_stop"
    )
)

# An event that represents a broadcasted request to confirm the destruction of the main window
BROADCAST_REQUEST_CONFIRM_MAIN_WINDOW_DESTROY: Final[DispatcherEvent] = (
    DispatcherEventFactory.create_dispatcher_event(
        name="broadcast_request_confirm_main_window_destroy"
    )
)

# An event that represents a broadcasted request to navigate backward in the UI
BROADCAST_REQUEST_UI_NAVIGATE_BACKWARD: Final[DispatcherEvent] = (
    DispatcherEventFactory.create_dispatcher_event(
        name="broadcast_request_ui_navigate_backward"
    )
)

# An event that represents a broadcasted request to navigate forward in the UI
BROADCAST_REQUEST_UI_NAVIGATE_FORWARD: Final[DispatcherEvent] = (
    DispatcherEventFactory.create_dispatcher_event(
        name="broadcast_request_ui_navigate_forward"
    )
)
