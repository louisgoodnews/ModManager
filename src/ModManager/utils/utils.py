"""
Author: Louis Goodnews
Date: 2025-09-01

A module containing utility functions used throughout the application.
"""

import random

from typing import Any, Dict, Final, Iterable, List, Union

from utils.constants import DISPATCHER


__all__: Final[List[str]] = [
    "count",
    "get_random_int",
    "is_empty",
    "is_even",
    "shuffle",
    "subscribe_to_events",
    "unsubscribe_from_events",
]


def count(iterable: Iterable[Any]) -> int:
    """
    Count the number of elements in an iterable.

    Args:
        iterable (Iterable[Any]): The iterable to count.

    Returns:
        int: The number of elements in the iterable.
    """

    # Return the number of elements in the iterable
    return len(iterable)


def get_random_int(
    max: int,
    min: int = 0,
) -> int:
    """
    Get a random integer between min and max.

    Args:
        max (int): The maximum value.
        min (int): The minimum value. Defaults to 0.

    Returns:
        int: A random integer between min and max.

    Raises:
        ValueError: If max is less than min.
    """

    # Check if max is less than min
    if max < min:
        # Raise ValueError if max is less than min
        raise ValueError("max must be greater than min")

    # Return a random integer between min and max
    return random.randint(
        a=min,
        b=max,
    )


def is_empty(iterable: Iterable[Any]) -> bool:
    """
    Check if an iterable is empty.

    Args:
        iterable (Iterable[Any]): The iterable to check.

    Returns:
        bool: True if the iterable is empty, False otherwise.
    """

    # Return True if the iterable is empty, False otherwise
    return len(iterable) == 0


def is_even(number: Union[float, int]) -> bool:
    """
    Check if a number is even.

    Args:
        number (Union[float, int]): The number to check. Can be a float or an int.

    Returns:
        bool: True if the number is even, False otherwise.
    """

    # Return True if the number is even, False otherwise
    return number % 2 == 0


def shuffle(iterable: Iterable[Any]) -> Iterable[Any]:
    """
    Shuffle an iterable in place.

    Args:
        iterable (Iterable[Any]): The iterable to shuffle.

    Returns:
        Iterable[Any]: The shuffled iterable.
    """

    # Return the shuffled iterable
    return random.shuffle(x=iterable)


def subscribe_to_events(
    subscriptions: List[Dict[str, Any]],
) -> List[str]:
    """
    Subscribe to events.

    Args:
        subscriptions (List[Dict[str, Any]]): The subscriptions to subscribe to.

    Returns:
        List[str]: The function IDs of the subscriptions.
    """

    # Initialize the function IDs list
    function_ids: List[str] = []

    # Iterate over the subscriptions list
    for subscription in subscriptions:
        # Subscribe to the event
        function_id: str = DISPATCHER.subscribe(
            event=subscription["event"],
            function=subscription["function"],
            namespace=subscription["namespace"],
            persistent=subscription["persistent"],
        )

        # Add the function ID to the function IDs list
        function_ids.append(function_id)

    # Return the function IDs list
    return function_ids


def unsubscribe_from_events(
    function_ids: List[str],
) -> None:
    """
    Unsubscribe from events.

    Args:
        function_ids (List[str]): The function IDs to unsubscribe from.

    Returns:
        None
    """

    # Iterate over the function IDs list
    for function_id in function_ids:
        # Unsubscribe from the event
        DISPATCHER.unsubscribe(function_id=function_id)

    # Clear the function IDs list
    function_ids.clear()
