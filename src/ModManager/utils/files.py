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

from typing import Any, Dict, Final, List, Union

from utils.logging import info, exception

__all__: Final[List[str]] = [
    "create_directory",
    "create_file",
    "create_symlink",
    "file_exists",
    "file_read",
    "file_remove",
    "file_write",
]


def create_directory(
    path: str,
) -> None:
    """
    Creates a directory at the specified path.

    :param path: The path to the directory to create.
    :type path: str

    :return: None
    :rtype: None
    """
    try:
        # Create the directory
        os.makedirs(
            name=path,
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
    path: str,
) -> None:
    """
    Creates a file at the specified path.

    :param path: The path to the file to create.
    :type path: str

    :return: None
    :rtype: None
    """
    try:
        # Create the file
        os.makedirs(
            name=path,
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
    source: str,
    target: str,
) -> None:
    """
    Creates a symbolic link from the source to the target.

    :param source: The path to the source file or directory.
    :type source: str

    :param target: The path to the target file or directory.
    :type target: str

    :return: None
    :rtype: None
    """

    # Check if the platform is not Windows
    if sys.platform != "win32":
        # Fallback to copy if link creation fails
        os.link(
            dst=target,
            src=source,
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
            dst=target,
            src=source,
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


def file_copy(
    source: str,
    target: str,
) -> None:
    """
    Copies a file from the source to the target.

    :param source: The path to the source file.
    :type source: str

    :param target: The path to the target file.
    :type target: str

    :return: None
    :rtype: None
    """
    try:
        # Copy the file
        shutil.copy(
            dst=target,
            src=source,
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


def file_exists(path: str) -> bool:
    """
    Checks if a file exists at the specified path.

    :param path: The path to the file to check.
    :type path: str

    :return: True if the file exists, False otherwise.
    :rtype: bool
    """
    return os.path.exists(path=path)


def file_read(path: str) -> Union[str, Dict[str, Any]]:
    """
    Reads the contents of a file at the specified path.

    :param path: The path to the file to read.
    :type path: str

    :return: The contents of the file as a string or dictionary.
    :rtype: Union[str, Dict[str, Any]]
    """

    async def __read__(path: str) -> Union[str, Dict[str, Any]]:
        """
        Reads the contents of a file at the specified path.

        :param path: The path to the file to read.
        :type path: str

        :return: The contents of the file as a string or dictionary.
        :rtype: Union[str, Dict[str, Any]]
        """

        try:
            async with aiofiles.open(
                encoding="utf-8",
                file=path,
                mode="r",
            ) as f:
                # Check if file is a JSON file
                if path.endswith(".json"):
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

    return asyncio.run(__read__(path=path))


def file_read_json(path: str) -> Dict[str, Any]:
    """
    Reads the contents of a JSON file at the specified path.

    :param path: The path to the JSON file to read.
    :type path: str

    :return: The contents of the JSON file as a dictionary.
    :rtype: Dict[str, Any]
    """
    return file_read(path=path)


def file_remove(path: str) -> None:
    """
    Removes a file at the specified path.

    :param path: The path to the file to remove.
    :type path: str

    :return: None
    :rtype: None
    """
    try:
        # Remove the file
        os.remove(path=path)

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
    path: str,
    data: st,
) -> None:
    """
    Writes the specified data to a file at the specified path.

    :param path: The path to the file to write to.
    :type path: str

    :param data: The data to write to the file.
    :type data: str

    :return: None
    :rtype: None
    """

    async def __write__(
        path: str,
        data: str,
    ) -> None:
        """
        Writes the specified data to a file at the specified path.

        :param path: The path to the file to write to.
        :type path: str

        :param data: The data to write to the file.
        :type data: str

        :return: None
        :rtype: None
        """

        try:
            async with aiofiles.open(
                encoding="utf-8",
                file=path,
                mode="w",
            ) as f:
                await f.write(data)
        except Exception as e:
            # Log exception
            exception(
                exception=e,
                message="Caught an exception while attempting to write file",
                name="files.file_write",
            )

    return asyncio.run(
        __write__(
            data=data,
            path=path,
        )
    )


def file_write_json(
    path: str,
    data: Dict[str, Any],
) -> None:
    """
    Writes the specified data to a JSON file at the specified path.

    :param path: The path to the JSON file to write to.
    :type path: str

    :param data: The data to write to the JSON file.
    :type data: Dict[str, Any]

    :return: None
    :rtype: None
    """
    file_write(
        path=path,
        data=json.dumps(data),
    )
