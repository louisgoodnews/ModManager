"""
Author: Louis Goodnews
Date: 2025-09-01

A module containing constants used throughout the application.
"""

from datetime import datetime
from tkinter.constants import *
from typing import Final, List, Literal, Tuple

from DateUtil import DateUtil
from Dispatcher import Dispatcher
from Logger import Logger


__all__: Final[List[str]] = [
    "APPLICATION_NAME",
    "DAY_AFTER_TOMORROW",
    "DAY_BEFORE_YESTERDAY",
    "DEFAULT_FONT",
    "DEFAULT_FONT_FAMILY",
    "DEFAULT_FONT_SIZE",
    "DEFAULT_GEOMETRY",
    "DISPATCHER",
    "END_OF_MONTH",
    "END_OF_WEEK",
    "GLOBAL",
    "LARGE_DEFAULT_FONT",
    "LARGE_FONT_SIZE",
    "LOGGER",
    "SMALL_DEFAULT_FONT",
    "SMALL_FONT_SIZE",
    "START_OF_MONTH",
    "START_OF_WEEK",
    "TODAY",
    "TOMORROW",
    "VERSION",
    "WINDOW_NAME",
    "YESTERDAY",
]


# Application name
APPLICATION_NAME: Final[Literal["ModManager"]] = "ModManager"

# Get the day after tomorrow's date
DAY_AFTER_TOMORROW: Final[datetime] = DateUtil.day_after_tomorrow()

# Get the day before yesterday's date
DAY_BEFORE_YESTERDAY: Final[datetime] = DateUtil.day_before_yesterday()

# Default font family
DEFAULT_FONT_FAMILY: Final[Literal["Helvetica"]] = "Helvetica"

# Default font size
DEFAULT_FONT_SIZE: Final[int] = 12

# Default font
DEFAULT_FONT: Final[Tuple[str, int]] = (
    DEFAULT_FONT_FAMILY,
    DEFAULT_FONT_SIZE,
)

# Default geometry
DEFAULT_GEOMETRY: Final[Literal["1980x1080+0+0"]] = "1980x1080+0+0"

# Initialize the application's Dispatcher instance
DISPATCHER: Final[Dispatcher] = Dispatcher()

# Get the end of the month
END_OF_MONTH: Final[datetime] = DateUtil.end_of_month()

# Get the end of the week
END_OF_WEEK: Final[datetime] = DateUtil.end_of_week()

# Global scope
GLOBAL: Final[Literal["global"]] = "global"

# Large font size
LARGE_FONT_SIZE: Final[int] = 16

# Large default font
LARGE_DEFAULT_FONT: Final[Tuple[str, int]] = (
    DEFAULT_FONT_FAMILY,
    LARGE_FONT_SIZE,
)

# Initialize the application's Logger instance
LOGGER: Final[Logger] = Logger.get_logger(name=APPLICATION_NAME)

# Small font size
SMALL_FONT_SIZE: Final[int] = 10

# Small default font
SMALL_DEFAULT_FONT: Final[Tuple[str, int]] = (
    DEFAULT_FONT_FAMILY,
    SMALL_FONT_SIZE,
)

# Get the start of the month
START_OF_MONTH: Final[datetime] = DateUtil.start_of_month()

# Get the start of the week
START_OF_WEEK: Final[datetime] = DateUtil.start_of_week()

# Get today's date
TODAY: Final[datetime] = DateUtil.today()

# Get tomorrow's date
TOMORROW: Final[datetime] = DateUtil.tomorrow()

# Application version
VERSION: Final[Literal["0.1.0"]] = "0.1.0"

# Window name
WINDOW_NAME: Final[Literal[f"{APPLICATION_NAME} (v. {VERSION})"]] = (
    f"{APPLICATION_NAME} (v. {VERSION})"
)

# Get yesterday's date
YESTERDAY: Final[datetime] = DateUtil.yesterday()
