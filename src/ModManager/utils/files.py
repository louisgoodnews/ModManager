"""
Author: Louis Goodnews
Date: 2025-08-12
"""

import aiofiles
import asyncio
import json
import os
import shutil
import sys

from pathlib import Path
from typing import Any, Dict, Final, List, Union

from utils.logging import info, exception

__all__: Final[List[str]] = [
    "create_directory",
    "create_file",
    "create_symlink",
    "directory_exists",
    "file_exists",
    "file_read",
    "file_remove",
    "file_write",
    "list_directory_contents",
    "remove_symlink",
    "symlink_exists",
]


def create_directory(
    path: Union[Path, str],
) -> None:
    """
    Creates a directory at the specified path.

    :param path: The path to the directory to create.
    :type path: Union[Path, str]

    :return: None
    :rtype: None
    """

    # Check if the path is a Path object
    if not isinstance(
        path,
        Path,
    ):
        # Convert the path to a Path object
        path = Path(path)

    try:
        # Create the directory
        os.makedirs(
            name=path.as_posix(),
            exist_ok=True,
        )

        # Log directory creation
        info(
            message=f"Created directory at {path}",
            name="files.create_directory",
        )
    except Exception as e:
        # Log exception
        exception(
            exception=e,
            message="Caught an exception while attempting to create directory",
            name="files.create_directory",
        )


def create_file(
    path: Union[Path, str],
) -> None:
    """
    Creates a file at the specified path.

    :param path: The path to the file to create.
    :type path: Union[Path, str]

    :return: None
    :rtype: None
    """

    # Check if the path is a Path object
    if not isinstance(
        path,
        Path,
    ):
        # Convert the path to a Path object
        path = Path(path)

    try:
        # Create the file
        os.makedirs(
            name=path.as_posix(),
            exist_ok=True,
        )

        # Log file creation
        info(
            message=f"Created file at {path}",
            name="files.create_file",
        )
    except Exception as e:
        # Log exception
        exception(
            exception=e,
            message="Caught an exception while attempting to create file",
            name="files.create_file",
        )


def create_symlink(
    source: Union[Path, str],
    target: Union[Path, str],
) -> None:
    """
    Creates a symbolic link from the source to the target.

    :param source: The path to the source file or directory.
    :type source: Union[Path, str]

    :param target: The path to the target file or directory.
    :type target: Union[Path, str]

    :return: None
    :rtype: None
    """

    # Check if the source is a Path object
    if not isinstance(
        source,
        Path,
    ):
        # Convert the source to a Path object
        source = Path(source)

    # Check if the target is a Path object
    if not isinstance(
        target,
        Path,
    ):
        # Convert the target to a Path object
        target = Path(target)

    # Check if the platform is not Windows
    if sys.platform != "win32":
        # Fallback to copy if link creation fails
        os.link(
            dst=target.as_posix(),
            src=source.as_posix(),
        )

        # Log link creation
        info(
            message=f"Created link from {source} to {target}",
            name="files.create_symlink",
        )

        # Return early if link creation is successful
        return

    try:
        os.symlink(
            dst=target.as_posix(),
            src=source.as_posix(),
            target_is_directory=True,
        )

        # Log symlink creation
        info(
            message=f"Created symlink from {source} to {target}",
            name="files.create_symlink",
        )
    except Exception as e:
        # Log exception
        exception(
            exception=e,
            message="Caught an exception while attempting to create symlink",
            name="files.create_symlink",
        )

        # Log fallback to copy
        info(
            message=f"Falling back to copy from {source} to {target}",
            name="files.create_symlink",
        )

        # Fallback to copy if symlink creation fails
        file_copy(
            source=source,
            target=target,
        )


def directory_exists(path: Union[Path, str]) -> bool:
    """
    Checks if a directory exists at the specified path.

    :param path: The path to the directory to check.
    :type path: Union[Path, str]

    :return: True if the directory exists, False otherwise.
    :rtype: bool
    """

    # Check if the path is a Path object
    if not isinstance(
        path,
        Path,
    ):
        # Convert the path to a Path object
        path = Path(path)

    # Check if the directory exists
    return path.exists()


def file_copy(
    source: Union[Path, str],
    target: Union[Path, str],
) -> None:
    """
    Copies a file from the source to the target.

    :param source: The path to the source file.
    :type source: Union[Path, str]

    :param target: The path to the target file.
    :type target: Union[Path, str]

    :return: None
    :rtype: None
    """

    # Check if the source is a Path object
    if not isinstance(
        source,
        Path,
    ):
        # Convert the source to a Path object
        source = Path(source)

    # Check if the target is a Path object
    if not isinstance(
        target,
        Path,
    ):
        # Convert the target to a Path object
        target = Path(target)

    try:
        # Copy the file
        shutil.copy(
            dst=target.as_posix(),
            src=source.as_posix(),
        )

        # Log file copy
        info(
            message=f"Copied file from {source} to {target}",
            name="files.file_copy",
        )
    except Exception as e:
        # Log exception
        exception(
            exception=e,
            message="Caught an exception while attempting to copy file",
            name="files.file_copy",
        )


def file_exists(path: Union[Path, str]) -> bool:
    """
    Checks if a file exists at the specified path.

    :param path: The path to the file to check.
    :type path: Union[Path, str]

    :return: True if the file exists, False otherwise.
    :rtype: bool
    """

    # Check if the path is a Path object
    if not isinstance(
        path,
        Path,
    ):
        # Convert the path to a Path object
        path = Path(path)

    # Check if the file exists
    return path.exists()


def file_read(path: Union[Path, str]) -> Union[str, Dict[str, Any]]:
    """
    Reads the contents of a file at the specified path.

    :param path: The path to the file to read.
    :type path: Union[Path, str]

    :return: The contents of the file as a string or dictionary.
    :rtype: Union[str, Dict[str, Any]]
    """

    async def __read__(path: Path) -> Union[str, Dict[str, Any]]:
        """
        Reads the contents of a file at the specified path.

        :param path: The path to the file to read.
        :type path: Path

        :return: The contents of the file as a string or dictionary.
        :rtype: Union[str, Dict[str, Any]]
        """

        try:
            async with aiofiles.open(
                encoding="utf-8",
                file=path.as_posix(),
                mode="r",
            ) as f:
                # Check if file is a JSON file
                if path.as_posix().endswith(".json"):
                    # Return JSON data
                    return json.loads(await f.read())

                # Return text data otherwise
                return await f.read()
        except Exception as e:
            # Log exception
            exception(
                exception=e,
                message="Caught an exception while attempting to read file",
                name="files.file_read",
            )
            return ""

    # Check if the path is a Path object
    if not isinstance(
        path,
        Path,
    ):
        # Convert the path to a Path object
        path = Path(path)

    return asyncio.run(__read__(path=path))


def file_read_json(path: Union[Path, str]) -> Dict[str, Any]:
    """
    Reads the contents of a JSON file at the specified path.

    :param path: The path to the JSON file to read.
    :type path: Union[Path, str]

    :return: The contents of the JSON file as a dictionary.
    :rtype: Dict[str, Any]
    """

    # Check if the path is a Path object
    if not isinstance(
        path,
        Path,
    ):
        # Convert the path to a Path object
        path = Path(path)

    return file_read(path=path)


def file_remove(path: Union[Path, str]) -> None:
    """
    Removes a file at the specified path.

    :param path: The path to the file to remove.
    :type path: Union[Path, str]

    :return: None
    :rtype: None
    """

    # Check if the path is a Path object
    if not isinstance(
        path,
        Path,
    ):
        # Convert the path to a Path object
        path = Path(path)

    try:
        # Remove the file
        os.remove(path=path.as_posix())

        # Log file removal
        info(
            message=f"Removed file at {path}",
            name="files.file_remove",
        )
    except Exception as e:
        # Log exception
        exception(
            exception=e,
            message="Caught an exception while attempting to remove file",
            name="files.file_remove",
        )


def file_write(
    path: Union[Path, str],
    data: str,
) -> None:
    """
    Writes the specified data to a file at the specified path.

    :param path: The path to the file to write to.
    :type path: Union[Path, str]

    :param data: The data to write to the file.
    :type data: str

    :return: None
    :rtype: None
    """

    async def __write__(
        path: Path,
        data: str,
    ) -> None:
        """
        Writes the specified data to a file at the specified path.

        :param path: The path to the file to write to.
        :type path: Path

        :param data: The data to write to the file.
        :type data: str

        :return: None
        :rtype: None
        """

        try:
            async with aiofiles.open(
                encoding="utf-8",
                file=path.as_posix(),
                mode="w",
            ) as f:
                # Write the data to the file
                await f.write(data)
        except Exception as e:
            # Log exception
            exception(
                exception=e,
                message="Caught an exception while attempting to write file",
                name="files.file_write",
            )

    # Check if the path is a Path object
    if not isinstance(
        path,
        Path,
    ):
        # Convert the path to a Path object
        path = Path(path)

    return asyncio.run(
        __write__(
            data=data,
            path=path,
        )
    )


def file_write_json(
    path: Union[Path, str],
    data: Dict[str, Any],
) -> None:
    """
    Writes the specified data to a JSON file at the specified path.

    :param path: The path to the JSON file to write to.
    :type path: Union[Path, str]

    :param data: The data to write to the JSON file.
    :type data: Dict[str, Any]

    :return: None
    :rtype: None
    """

    # Check if the path is a Path object
    if not isinstance(
        path,
        Path,
    ):
        # Convert the path to a Path object
        path = Path(path)

    # Write the data to the file
    file_write(
        path=path,
        data=json.dumps(data),
    )


def list_directory_contents(path: Union[Path, str]) -> List[Dict[str, Any]]:
    """
    Lists the contents of a directory at the specified path.

    :param path: The path to the directory to list.
    :type path: Union[Path, str]

    :return: A list of dictionaries containing the contents of the directory.
    :rtype: List[Dict[str, Any]]
    """

    # Check if the path is a Path object
    if not isinstance(
        path,
        Path,
    ):
        # Convert the path to a Path object
        path = Path(path)

    # List the contents of the directory
    return [
        {
            "file_type": file.suffix,
            "name": file.name,
            "is_dir": file.is_dir(),
        }
        for file in path.iterdir()
    ]


def remove_symlink(path: Union[Path, str]) -> None:
    """
    Removes a symlink at the specified path.

    :param path: The path to the symlink to remove.
    :type path: Union[Path, str]

    :return: None
    :rtype: None
    """

    # Check if the path is a Path object
    if not isinstance(
        path,
        Path,
    ):
        # Convert the path to a Path object
        path = Path(path)

    # Remove the symlink
    os.remove(path=path.as_posix())


def symlink_exists(path: Union[Path, str]) -> bool:
    """
    Checks if a symlink exists at the specified path.

    :param path: The path to the symlink to check.
    :type path: Union[Path, str]

    :return: True if the symlink exists, False otherwise.
    :rtype: bool
    """

    # Check if the path is a Path object
    if not isinstance(
        path,
        Path,
    ):
        # Convert the path to a Path object
        path = Path(path)

    # Check if the symlink exists
    return path.exists(follow_symlinks=False)
