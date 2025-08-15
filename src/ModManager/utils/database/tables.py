"""
Author: Louis Goodnews
Date: 2025-08-15
"""

from typing import Any, Dict, Final, List

from utils.sqlite import get_sqlite_column

__all__: Final[List[str]] = [
    "GAMES_TABLE",
    "MODS_TABLE",
]


GAMES_TABLE: Final[Dict[str, Any]] = {
    "id": get_sqlite_column(
        name="id",
        primary_key=True,
        type="INTEGER",
        unique=True,
    ),
    "code": get_sqlite_column(
        name="code",
        type="TEXT",
        unique=True,
    ),
    "last_loaded_at": get_sqlite_column(
        name="last_loaded_at",
        type="TIMESTAMP",
    ),
    "mod_archive_location": get_sqlite_column(
        name="mod_archive_location",
        type="TEXT",
    ),
    "mod_install_location": get_sqlite_column(
        name="mod_install_location",
        type="TEXT",
    ),
    "name": get_sqlite_column(
        name="name",
        type="TEXT",
        unique=True,
    ),
    "nexus_id": get_sqlite_column(
        name="nexus_id",
        type="TEXT",
        unique=True,
    ),
    "path": get_sqlite_column(
        name="path",
        type="TEXT",
        unique=True,
    ),
    "registered_at": get_sqlite_column(
        name="registered_at",
        type="TIMESTAMP",
    ),
}

MODS_TABLE: Final[Dict[str, Any]] = {
    "id": get_sqlite_column(
        name="id",
        primary_key=True,
        type="INTEGER",
        unique=True,
    ),
    "game": get_sqlite_column(
        name="game",
        foreign_key="games(id)",
        on_delete="CASCADE",
        on_update="CASCADE",
        type="INTEGER",
    ),
    "name": get_sqlite_column(
        name="name",
        type="TEXT",
        unique=True,
    ),
    "nexus_id": get_sqlite_column(
        name="nexus_id",
        type="TEXT",
        unique=True,
    ),
    "path": get_sqlite_column(
        name="path",
        type="TEXT",
        unique=True,
    ),
    "registered_at": get_sqlite_column(
        name="registered_at",
        type="TIMESTAMP",
    ),
    "uuid": get_sqlite_column(
        name="uuid",
        type="TEXT",
        unique=True,
    ),
    "version": get_sqlite_column(
        name="version",
        type="TEXT",
    ),
}
