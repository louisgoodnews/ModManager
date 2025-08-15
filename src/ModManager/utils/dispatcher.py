"""
Author: Louis Goodnews
Date: 2025-08-12
"""

import uuid

from typing import Any, Callable, Dict, Final, List, Union

from utils.logging import exception

__all__: Final[List[str]] = [
    "dispatch",
    "register",
    "unregister",
]


SUBSCRIPTIONS: Final[Dict[str, Dict[str, List[Dict[str, Any]]]]] = {}


def dispatch(
    event: str,
    namespace: str,
    *args,
    **kwargs,
) -> Dict[str, Any]:
    """
    Dispatches an event to all registered functions.

    :param event: The event to dispatch.
    :type event: str
    :param namespace: The namespace to dispatch the event to.
    :type namespace: str
    :param args: The arguments to pass to the functions.
    :type args: Any
    :param kwargs: The keyword arguments to pass to the functions.
    :type kwargs: Any

    :return: A dictionary containing the results of the dispatched functions.
    :rtype: Dict[str, Any]
    """

    # Initialize the result dictionary
    result: Dict[str, Any] = {}

    # Check if the event is registered
    if event not in SUBSCRIPTIONS:
        # Return the result dictionary
        return result

    # Check if the namespace is registered
    if namespace not in SUBSCRIPTIONS.get(
        event,
        {},
    ):
        # Return the result dictionary
        return result

    # Initialize the non-persistent list
    non_persistenta: List[str] = []

    # Iterate over the subscriptions
    for subscription in SUBSCRIPTIONS[event][namespace]:
        try:
            # Call the function
            result[subscription["function"].__name__] = subscription["function"](
                event=event,
                *args,
                **kwargs,
            )
        except Exception as e:
            # Log the exception
            exception(
                exception=e,
                message=f"Caught an exception while attempting to dispatch event '{event}' to function '{subscription['function']}'.",
                name="dispatcher.dispatch",
            )

        # Check if the subscription is non-persistent
        if not subscription["persistent"]:
            # Add the registration ID to the non-persistent list
            non_persistenta.append(subscription["registration_id"])

    # Unregister the non-persistent subscriptions
    for registration_id in non_persistenta:
        # Unregister the subscription
        unregister(registration_id)

    # Return the result dictionary
    return result


def register(
    event: str,
    function: Callable[[Any], Any],
    namespace: str,
    persistent: bool = False,
) -> Union[bool, str]:
    """
    Registers a function to be called when an event is dispatched.

    :param event: The event to register the function for.
    :type event: str

    :param function: The function to be called when the event is dispatched.
    :type function: Callable[[Any], Any]

    :param namespace: The namespace to register the function for.
    :type namespace: str

    :param persistent: Whether the function should be called every time the event is dispatched.
        Defaults to False.
    :type persistent: bool

    :return: The registration ID if successful, False otherwise.
    :rtype: Union[bool, str]
    """

    # Check if the event is already registered
    if event not in SUBSCRIPTIONS:
        # Register the event
        SUBSCRIPTIONS[event] = {}

    # Check if the namespace is already registered
    if namespace not in SUBSCRIPTIONS[event]:
        # Register the namespace
        SUBSCRIPTIONS[event][namespace] = []

    # Generate a registration ID
    registration_id: str = str(uuid.uuid4())

    # Register the function
    SUBSCRIPTIONS[event][namespace].append(
        {
            "function": function,
            "persistent": persistent,
            "registration_id": registration_id,
        }
    )

    # Return the registration ID
    return registration_id


def unregister(registration_id: str) -> bool:
    """
    Unregisters a function from an event.

    :param registration_id: The registration ID of the function to unregister.
    :type registration_id: str

    :return: True if successful, False otherwise.
    :rtype: bool
    """

    # Iterate over the subscriptions
    for subscription in SUBSCRIPTIONS.values():
        # Iterate over the namespaces
        for namespace in subscription.values():
            # Iterate over the functions
            for function in namespace:
                # Check if the registration ID matches
                if function["registration_id"] != registration_id:
                    # Skip the subscription
                    continue

                # Remove the subscription
                namespace.remove(function)

                # Return True if successful
                return True

    # Return False if the registration ID was not found
    return False
