"""
Author: Louis Goodnews
Date: 2025-08-14
"""

import os
import sys

from pathlib import Path
from typing import Final, List


__all__: Final[List[str]] = [
    "API_JSON_PATH",
    "CWD_PATH",
    "DATA_PATH",
    "DATABASE_PATH",
    "DEFAULT_FONT",
    "DEFAULT_FONT_SIZE",
    "DOWNLOAD_PATH",
    "HOME_PATH",
    "MOD_ARCHIVES_PATH",
    "MODS_PATH",
    "MOD_INSTALLED_PATH",
    "PLATFORM",
]


CWD_PATH: Final[Path] = Path(os.getcwd())

API_JSON_PATH: Final[Path] = Path(
    os.path.join(
        CWD_PATH,
        "api.json",
    )
)

DATA_PATH: Final[Path] = Path(
    os.path.join(
        CWD_PATH,
        "data",
    )
)

DATABASE_PATH: Final[Path] = Path(
    os.path.join(
        DATA_PATH,
        "db.db",
    )
)

MODS_PATH: Final[Path] = Path(
    os.path.join(
        DATA_PATH,
        "mods",
    )
)

MOD_ARCHIVES_PATH: Final[Path] = Path(
    os.path.join(
        MODS_PATH,
        "archives",
    )
)

MOD_INSTALLED_PATH: Final[Path] = Path(
    os.path.join(
        MODS_PATH,
        "installed",
    )
)

HOME_PATH: Final[Path] = Path(os.path.expanduser("~"))

DOWNLOAD_PATH: Final[Path] = Path(
    os.path.join(
        HOME_PATH,
        "Downloads",
    )
)

DEFAULT_FONT: Final[str] = "Helvetica"

DEFAULT_FONT_SIZE: Final[int] = 12

PLATFORM: Final[str] = str(sys.platform)
