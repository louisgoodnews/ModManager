"""
Author: Louis Goodnews
Date: 2025-08-10
"""

import traceback

from datetime import datetime
from threading import RLock
from typing import Any, Dict, Final, List, Literal, Optional

__all__: Final[List[str]] = [
    "critical",
    "debug",
    "error",
    "exception",
    "fatal",
    "info",
    "log",
    "silent",
    "trace",
    "warn",
]


COLORIZATION: Dict[str, Any] = {
    "CRITICAL": "\033[95m",
    "FATAL": "\033[95m",
    "ERROR": "\033[91m",
    "EXCEPTION": "\033[91m",
    "WARN": "\033[93m",
    "INFO": "\033[92m",
    "DEBUG": "\033[94m",
    "TRACE": "\033[90m",
    "SILENT": "\033[0m",
}

RESET_COLOR: str = "\033[0m"

LOCK: RLock = RLock()


def log(
    level: Literal[
        "CRITICAL",
        "DEBUG",
        "ERROR",
        "EXCEPTION",
        "FATAL",
        "INFO",
        "SILENT",
        "TRACE",
        "WARN",
    ],
    message: str,
    name: str,
    exception: Optional[Exception] = None,
    *args,
    **kwargs,
) -> None:
    """
    Logs a formatted message with a specified severity level and optional exception information.

    The log message is printed to the console with a timestamp, log level, and a name identifier.
    Supports optional message formatting with positional and keyword arguments, and thread-safe output.
    The message is color-coded in the console based on the log level.

    Args:
        level (Literal): The severity level of the log message.
            Valid values are "CRITICAL", "DEBUG", "ERROR", "EXCEPTION", "FATAL", "INFO", "SILENT", "TRACE", and "WARN".
        message (str): The log message format string. Can include placeholders for formatting.
        name (str): A name identifier, typically indicating the source or module generating the log.
        exception (Optional[Exception], optional): An optional Exception instance.
            If provided, the exception's traceback will be appended to the log output. Defaults to None.
        *args: Positional arguments for formatting the message string.
        **kwargs: Keyword arguments for formatting the message string.

    Returns:
        None

    Example:
        log("INFO", "User {user} logged in", "AuthModule", user="Alice")
        log("ERROR", "Failed to open file: {}", "FileLoader", exception=exc, filename="data.txt")
    """

    if args:
        try:
            message = message.format(*args)
        except Exception:
            message = str(message)

    if kwargs:
        try:
            message = message.format(**kwargs)
        except Exception:
            message = str(message)

    if exception:
        message += f"\n{''.join(traceback.format_exception(type(exception), exception, exception.__traceback__))}"

    with LOCK:
        print(
            f"{COLORIZATION.get(level, RESET_COLOR)}{datetime.now().isoformat(timespec='milliseconds')} | {level.upper()} | {name} | {message}{RESET_COLOR}"
        )


def critical(
    message: str,
    name: str,
    *args,
    **kwargs,
) -> None:
    """
    Logs a message with the CRITICAL severity level.

    This is a convenience wrapper around the main log function,
    specifically setting the log level to "CRITICAL".

    Args:
        message (str): The log message format string. Can include placeholders for formatting.
        name (str): A name identifier, typically indicating the source or module generating the log.
        *args: Positional arguments for formatting the message string.
        **kwargs: Keyword arguments for formatting the message string.

    Returns:
        None

    Example:
        critical("System failure at {time}", "SystemMonitor", time="12:34")
    """
    log(
        level="CRITICAL",
        message=message,
        name=name,
        *args,
        **kwargs,
    )


def debug(
    message: str,
    name: str,
    *args,
    **kwargs,
) -> None:
    """
    Logs a message with the DEBUG severity level.

    This function serves as a convenience wrapper around the main log function,
    explicitly setting the log level to "DEBUG". It is intended for detailed
    diagnostic information useful during development and troubleshooting.

    Args:
        message (str): The log message format string. Can include placeholders for formatting.
        name (str): A name identifier, typically indicating the source or module generating the log.
        *args: Positional arguments for formatting the message string.
        **kwargs: Keyword arguments for formatting the message string.

    Returns:
        None

    Example:
        debug("Variable x has value: {}", "CalculationModule", x)
    """
    log(
        level="DEBUG",
        message=message,
        name=name,
        *args,
        **kwargs,
    )


def error(
    message: str,
    name: str,
    *args,
    **kwargs,
) -> None:
    """
    Logs a message with the ERROR severity level.

    This function is a convenience wrapper around the main log function,
    setting the log level to "ERROR". It is used to indicate serious issues
    or failures that require attention.

    Args:
        message (str): The log message format string. Can include placeholders for formatting.
        name (str): A name identifier, typically indicating the source or module generating the log.
        *args: Positional arguments for formatting the message string.
        **kwargs: Keyword arguments for formatting the message string.

    Returns:
        None

    Example:
        error("Failed to connect to database: {}", "DatabaseConnector", err_msg)
    """
    log(
        level="ERROR",
        message=message,
        name=name,
        *args,
        **kwargs,
    )


def exception(
    exception: Exception,
    message: str,
    name: str,
    *args,
    **kwargs,
) -> None:
    """
    Logs a message with the EXCEPTION severity level, including the traceback of an exception.

    This function is a convenience wrapper around the main log function,
    explicitly setting the log level to "EXCEPTION" and appending the
    formatted stack trace of the provided exception to the log output.

    Args:
        exception (Exception): The exception instance to be logged along with its traceback.
        message (str): The log message format string. Can include placeholders for formatting.
        name (str): A name identifier, typically indicating the source or module generating the log.
        *args: Positional arguments for formatting the message string.
        **kwargs: Keyword arguments for formatting the message string.

    Returns:
        None

    Example:
        try:
            result = 10 / 0
        except Exception as exc:
            exception(exc, "An error occurred while dividing", "MathModule")
    """
    log(
        exception=exception,
        level="EXCEPTION",
        message=message,
        name=name,
        *args,
        **kwargs,
    )


def fatal(
    message: str,
    name: str,
    *args,
    **kwargs,
) -> None:
    """
    Logs a message with the FATAL severity level.

    This function serves as a convenience wrapper around the main log function,
    setting the log level to "FATAL". It is intended for very severe error
    events that will presumably lead the application to abort.

    Args:
        message (str): The log message format string. Can include placeholders for formatting.
        name (str): A name identifier, typically indicating the source or module generating the log.
        *args: Positional arguments for formatting the message string.
        **kwargs: Keyword arguments for formatting the message string.

    Returns:
        None

    Example:
        fatal("Unrecoverable error occurred: {}", "SystemMonitor", error_msg)
    """
    log(
        level="FATAL",
        message=message,
        name=name,
        *args,
        **kwargs,
    )


def info(
    message: str,
    name: str,
    *args,
    **kwargs,
) -> None:
    """
    Logs a message with the INFO severity level.

    This function is a convenience wrapper around the main log function,
    setting the log level to "INFO". It is typically used for general
    informational messages that highlight the progress of the application.

    Args:
        message (str): The log message format string. Can include placeholders for formatting.
        name (str): A name identifier, typically indicating the source or module generating the log.
        *args: Positional arguments for formatting the message string.
        **kwargs: Keyword arguments for formatting the message string.

    Returns:
        None

    Example:
        info("User {user} logged in", "AuthModule", user="Alice")
    """
    log(
        level="INFO",
        message=message,
        name=name,
        *args,
        **kwargs,
    )


def silent(
    message: str,
    name: str,
    *args,
    **kwargs,
) -> None:
    """
    Logs a message with the SILENT severity level.

    This function is a convenience wrapper around the main log function,
    setting the log level to "SILENT". Messages logged with this level
    do not have any special visual highlighting (no color), appearing
    as normal text in the console.

    Args:
        message (str): The log message format string. Can include placeholders for formatting.
        name (str): A name identifier, typically indicating the source or module generating the log.
        *args: Positional arguments for formatting the message string.
        **kwargs: Keyword arguments for formatting the message string.

    Returns:
        None

    Example:
        silent("Background task started", "WorkerModule")
    """
    log(
        level="SILENT",
        message=message,
        name=name,
        *args,
        **kwargs,
    )


def trace(
    message: str,
    name: str,
    *args,
    **kwargs,
) -> None:
    """
    Logs a message with the TRACE severity level.

    This function is a convenience wrapper around the main log function,
    setting the log level to "TRACE". It is intended for very detailed
    diagnostic information, often more granular than DEBUG.

    Args:
        message (str): The log message format string. Can include placeholders for formatting.
        name (str): A name identifier, typically indicating the source or module generating the log.
        *args: Positional arguments for formatting the message string.
        **kwargs: Keyword arguments for formatting the message string.

    Returns:
        None

    Example:
        trace("Entering function {func_name}", "Tracer", func_name="my_func")
    """
    log(
        level="TRACE",
        message=message,
        name=name,
        *args,
        **kwargs,
    )


def warn(
    message: str,
    name: str,
    *args,
    **kwargs,
) -> None:
    """
    Logs a message with the WARN severity level.

    This function is a convenience wrapper around the main log function,
    setting the log level to "WARN". It is used to indicate potentially
    harmful situations or warnings that deserve attention.

    Args:
        message (str): The log message format string. Can include placeholders for formatting.
        name (str): A name identifier, typically indicating the source or module generating the log.
        *args: Positional arguments for formatting the message string.
        **kwargs: Keyword arguments for formatting the message string.

    Returns:
        None

    Example:
        warn("Low disk space: {}% remaining", "DiskMonitor", 5)
    """
    log(
        level="WARN",
        message=message,
        name=name,
        *args,
        **kwargs,
    )
