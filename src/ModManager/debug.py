"""
Author: Louis Goodnews
Date: 2025-08-10
"""

from utils.database.mods import get_mod_by_id
from utils.logging import debug


def main() -> None:
    """ """

    debug(
        message=get_mod_by_id(mod_id=1),
        name=__name__,
    )


if __name__ == "__main__":
    main()
