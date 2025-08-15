"""
Author: Louis Goodnews
Date: 2025-08-15
"""

import asyncio
import os

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Final, List, Optional, Union
from uuid import uuid4

from utils.constants import MOD_ARCHIVES_PATH, MOD_INSTALLED_PATH
from utils.database.tables import MODS_TABLE
from utils.logging import exception, info, warn
from utils.sqlite import (
    create_insert_sql_string,
    create_table_sql_string,
    execute_query,
    fetch_all,
    fetch_one,
    get_sqlite_table,
    insert,
    update,
)


__all__: Final[List[str]] = [
    "create_mods_table",
    "get_all_mods",
    "get_mod_by_code",
    "get_mod_by_id",
    "get_mods_by_ids",
    "get_mods_by_codes",
    "insert_mod",
    "update_mod",
]


def create_mods_table() -> None:
    """
    Creates the mods table in the database.

    :return: None
    :rtype: None
    """
    try:
        # Create the table
        asyncio.run(
            execute_query(
                query=create_table_sql_string(
                    table=get_sqlite_table(
                        columns=MODS_TABLE.values(),
                        name="mods",
                    )
                )
            )
        )
    except Exception as e:
        # Log the exception
        exception(
            exception=e,
            message="Failed to create mods table",
            name="mods.create_mods_table",
        )
