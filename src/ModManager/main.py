"""
Author: Louis Goodnews
Date: 2025-09-01
"""

from typing import Final, List

from core.core import Application


__all__: Final[List[str]] = []


def main() -> None:
    """
    The main function.

    Returns:
        None
    """

    # Initialize the application
    application: Final[Application] = Application()

    # Start the application
    application.start()

    # Shutdown the application
    application.shutdown()


if __name__ == "__main__":
    main()
