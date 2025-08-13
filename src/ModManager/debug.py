"""
Author: Louis Goodnews
Date: 2025-08-10
"""

import os

from core.core import API_JSON, load_api_json

from utils.logging import (
    critical,
    debug,
    error,
    exception,
    fatal,
    info,
    silent,
    trace,
    warn,
)
from utils.http import http_get, http_post, http_put
from utils.nexus_http import validate_api_key
from utils.sqlite import get_sqlite_column


def main() -> None:
    """ """

    critical(
        message="This is a critical message",
        name=__name__,
    )

    debug(
        message="This is a debug message",
        name=__name__,
    )

    error(
        message="This is an error message",
        name=__name__,
    )

    exception(
        exception=Exception("Example error"),
        message="Exception occurred",
        name=__name__,
    )

    fatal(
        message="This is a fatal message",
        name=__name__,
    )

    info(
        message="This is an info message",
        name=__name__,
    )

    silent(
        message="This is a silent message",
        name=__name__,
    )

    trace(
        message="This is a trace message",
        name=__name__,
    )

    warn(
        message="This is a warning message",
        name=__name__,
    )

    debug(
        message=http_get(
            url="https://httpbin.org/get",
        ),
        name=__name__,
    )

    debug(
        message=http_post(
            url="https://httpbin.org/post",
        ),
        name=__name__,
    )

    debug(
        message=http_put(
            url="https://httpbin.org/put",
        ),
        name=__name__,
    )

    debug(
        message=get_sqlite_column(
            name="mods",
            type="JSON",
        ),
        name=__name__,
    )

    debug(
        message=os.path.join(
            os.getcwd(),
            "data",
            "db.db",
        ),
        name=__name__,
    )

    debug(
        message=validate_api_key(
            api_key="",
        ),
        name=__name__,
    )

    load_api_json()

    debug(
        message=API_JSON,
        name=__name__,
    )


if __name__ == "__main__":
    main()
