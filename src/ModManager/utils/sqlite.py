"""
Author: Loius Goodnews
Date: 2025-08-10
"""

import aiosqlite

from typing import Any, Dict, Final, List, Literal, Optional

from utils.constants import DATABASE_PATH
from utils.logging import exception

__all__: Final[List[str]] = [
    "column_to_sql_string",
    "create_insert_sql_string",
    "create_table_sql_string",
    "delete",
    "execute_query",
    "fetch_all",
    "fetch_one",
    "get_sqlite_column",
    "get_sqlite_table",
    "insert",
    "update",
]


def column_to_sql_string(column: Dict[str, Any]) -> str:
    """
    Converts a column definition dictionary into an SQLite column definition SQL string.

    Args:
        column (Dict[str, Any]): A dictionary defining the column properties,
            as returned by `get_sqlite_column`.

    Returns:
        str: A string containing the SQLite SQL fragment for this column.

    Example:
        column = get_sqlite_column(
            name="id",
            type="INTEGER",
            primary_key=True,
            unique=True,
            default=None,
        )
        sql_str = column_to_sql_string(column)
        # sql_str -> 'id INTEGER PRIMARY KEY UNIQUE'

    Notes:
        - Foreign key constraints are not included in the column definition string
          as SQLite defines foreign keys separately.
        - Default values are quoted as needed depending on their type.
    """

    parts: List[str] = [
        column["name"],
        column["type"],
    ]

    if column.get(
        "primary_key",
        None,
    ):
        parts.append("PRIMARY KEY")

    if column.get(
        "unique",
        None,
    ):
        parts.append("UNIQUE")

    default: Optional[Any] = column.get(
        "default",
        None,
    )

    if default is not None:
        if isinstance(
            default,
            str,
        ):
            default_val: str = f"'{default}'"
        elif isinstance(
            default,
            bool,
        ):
            default_val: str = "1" if default else "0"
        else:
            default_val: str = str(default)
        parts.append(f"DEFAULT {default_val}")

    foreign_key = column.get(
        "foreign_key",
        None,
    )

    if foreign_key:
        parts.append(f"REFERENCES {foreign_key}")

        on_delete: str = column.get(
            "on_delete",
            "NO_ACTION",
        ).upper()

        if on_delete in (
            "CASCADE",
            "NO_ACTION",
            "RESTRICT",
            "SET_NULL",
        ):
            parts.append(f"ON DELETE {on_delete}")

        on_update: str = column.get(
            "on_update",
            "NO_ACTION",
        ).upper()

        if on_update in (
            "CASCADE",
            "NO_ACTION",
            "RESTRICT",
            "SET_NULL",
        ):
            parts.append(f"ON UPDATE {on_update}")

    nullable: bool = column.get(
        "nullable",
        True,
    )

    if not nullable:
        parts.append("NOT NULL")

    return " ".join(parts)


def create_insert_sql_string(table: Dict[str, Any]) -> str:
    """
    Generates an SQL INSERT statement with placeholders for the given table definition.

    Args:
        table (Dict[str, Any]): Table definition dictionary with keys:
            - "name": Name of the table (str)
            - "columns": List of column dicts, each with at least a "name" key.

    Returns:
        str: SQL INSERT statement string with parameter placeholders.

    Example:
        For table = {
            "name": "users",
            "columns": [
                {"name": "id", ...},
                {"name": "username", ...},
                {"name": "email", ...},
            ],
        }

        The function returns:
        "INSERT INTO users (id, username, email) VALUES (?, ?, ?);"
    """

    return f"INSERT INTO {table['name']} ({", ".join(column['name'] for column in table.get("columns", {}))}) VALUES ({", ".join(["?"] * len(table.get("columns", {})))})"


def create_table_sql_string(table: Dict[str, Any]) -> str:
    """
    Generates a SQLite CREATE TABLE SQL statement from a table definition dictionary.

    Args:
        table (Dict[str, Any]): A dictionary representing the table schema. Expected keys:
            - "name" (str): The name of the table.
            - "columns" (List[Dict[str, Any]]): A list of column definitions, where each
              column is a dictionary with attributes such as name, type, constraints, etc.
              Each column dictionary should be compatible with the `column_to_sql_string` function.

    Returns:
        str: A string containing the full SQL CREATE TABLE statement, including
        all columns, with 'IF NOT EXISTS' to avoid errors if the table already exists.

    Notes:
        - This function relies on `column_to_sql_string` to convert individual column
          definitions into their corresponding SQL snippets.
        - The returned SQL statement does not include table-level constraints such as
          foreign keys or indexes; these should be handled separately if needed.
        - The formatting uses newlines between columns for readability.
    """

    return f"CREATE TABLE IF NOT EXISTS {table['name']}\n({',\n'.join([column_to_sql_string(column=column) for column in table.get('columns', [])])});"


async def delete(
    query: str,
    params: Optional[List[Any]] = None,
) -> Optional[int]:
    """
    Executes an asynchronous SQL DELETE statement on the SQLite database.

    This function is intended for DELETE queries that remove rows from a table.
    It opens an asynchronous connection to the database, executes the query with optional parameters,
    commits the transaction, and returns the number of rows deleted.

    Args:
        query (str): The SQL DELETE query string to execute.
        params (Optional[List[Any]], optional): A list of parameters to safely substitute into the query.
            Defaults to None.

    Returns:
        Optional[int]: The number of rows deleted. Returns None if the deletion failed.

    Raises:
        Exception: Any exception occurring during database connection, query execution,
        or commit will be caught and logged via the `exception` logger method.

    Notes:
        - Parameterized queries are strongly recommended to avoid SQL injection.
    """

    try:
        # Create and return a connection proxy to the sqlite database.
        async with aiosqlite.connect(database=DATABASE_PATH) as db:
            # Create a cursor and execute the given query
            cursor: aiosqlite.Cursor = await db.execute(
                parameters=params or [],
                sql=query,
            )

            # Commit the current transaction.
            await db.commit()

            # Return the count of affected rows.
            return cursor.rowcount
    except Exception as e:
        # Log an exception
        exception(
            exception=e,
            message=f"Caught an exception while attempting to delete with query '{query}' and parameters {params}.",
            name="sqlite.delete",
        )

        # Return None indicating that an exceptino occurred
        return None


async def execute_query(
    query: str,
    params: Optional[List[Any]] = None,
) -> None:
    """
    Executes a given SQL query asynchronously on the SQLite database without returning any result.

    This function is intended for SQL statements that modify the database state,
    such as CREATE, INSERT, UPDATE, or DELETE. It opens an asynchronous connection
    to the database, executes the provided query with optional parameters, and commits the transaction.

    Args:
        query (str): The SQL query string to execute.
        params (Optional[List[Any]], optional): A list of parameters to safely substitute into the query.
            Defaults to None.

    Raises:
        Exception: Any exception that occurs during database connection, query execution, or commit
        will be caught and logged via the `exception` logger method.

    Notes:
        - This method does not return any data.
        - The caller should ensure that the query is valid and parameters match the placeholders.
        - Parameterized queries are strongly recommended to avoid SQL injection.
    """

    try:
        # Create and return a connection proxy to the sqlite database.
        async with aiosqlite.connect(database=DATABASE_PATH) as db:
            # Helper to create a cursor and execute the given query.
            await db.execute(
                parameters=params or [],
                sql=query,
            )

            # Commit the current transaction
            await db.commit()
    except Exception as e:
        # Log the exception
        exception(
            exception=e,
            message="Caught an exception while attempting to execute query '{query}' with parameters {params}.",
            name="sqlite.execute_qiery",
        )


async def fetch_all(
    query: str,
    params: Optional[List[Any]] = None,
) -> Optional[List[Dict[str, Any]]]:
    """
    Executes an asynchronous SQL query on the SQLite database and fetches all rows.

    This function is intended for SELECT queries where multiple rows may be returned.
    It opens an asynchronous connection to the database, executes the query with optional parameters,
    and returns all result rows as a list of dictionaries.

    Args:
        query (str): The SQL query string to execute.
        params (Optional[List[Any]], optional): A list of parameters to safely substitute into the query.
            Defaults to None.

    Returns:
        Optional[List[Dict[str, Any]]]: A list of dictionaries representing all rows of the result,
        with column names as keys. Returns None if no rows were found.

    Raises:
        Exception: Any exception occurring during database connection, query execution,
        or fetching the results will be caught and logged via the `exception` logger method.

    Notes:
        - Parameterized queries are strongly recommended to avoid SQL injection.
        - This method returns all rows. For a single row, use a method like `fetch_one`.
    """

    try:
        # Create and return a connection proxy to the sqlite database.
        async with aiosqlite.connect(database=DATABASE_PATH) as db:
            # Making sure that the result is returned as a dict-like object
            db.row_factory = aiosqlite.Row

            # Helper to create a cursor and execute the given query.
            async with db.execute(
                parameters=params or [],
                sql=query,
            ) as cursor:
                # Fetch all rows
                rows: Optional[List[aiosqlite.Row]] = await cursor.fetchall()

                # Check if any rows exist
                if not rows:
                    # Return None if no rows found
                    return None

                # Return a list of dictionary representations of the rows to the caller
                return [dict(row) for row in rows]
    except Exception as e:
        # Log the exception
        exception(
            exception=e,
            message=f"Caught an exception while attempting to fetch all rows with query '{query}' and parameters {params}.",
            name="sqlite.fetch_all",
        )

        # Return None indicating that an exception has occurred
        return None


async def fetch_one(
    query: str,
    params: Optional[List[Any]] = None,
) -> Optional[Dict[str, Any]]:
    """
    Executes an asynchronous SQL query on the SQLite database and fetches a single row.

    This function is intended for SELECT queries where only one row is expected.
    It opens an asynchronous connection to the database, executes the query with optional parameters,
    and returns the first result row as a dictionary.

    Args:
        query (str): The SQL query string to execute.
        params (Optional[List[Any]], optional): A list of parameters to safely substitute into the query.
            Defaults to None.

    Returns:
        Optional[Dict[str, Any]]: A dictionary representing the first row of the result,
        with column names as keys. Returns None if no row was found.

    Raises:
        Exception: Any exception occurring during database connection, query execution,
        or fetching the result will be caught and logged via the `exception` logger method.

    Notes:
        - Parameterized queries are strongly recommended to avoid SQL injection.
        - This method returns only a single row. For multiple rows, use a method like `fetch_all`.
    """

    try:
        # Create and return a connection proxy to the sqlite database.
        async with aiosqlite.connect(database=DATABASE_PATH) as db:
            # Making sure that the result is returned as a dict-like object
            db.row_factory = aiosqlite.Row

            # Helper to create a cursor and execute the given query.
            async with db.execute(
                parameters=params or [],
                sql=query,
            ) as cursor:
                # Fetch a single row
                row: Optional[aiosqlite.Row] = await cursor.fetchone()

                # Check if the row esists
                if not row:
                    # Return None if the row does not exist
                    return None

                # Return a dictionary representation of the row to the caller
                return dict(row)
    except Exception as e:
        # Log the exception
        exception(
            exception=e,
            message=f"Caught an exception while attempting to fetch one row with query '{query}' and parameters {params}.",
            name="sqlite.fetch_one",
        )

        # Return None indicating that an exception has occurred
        return None


def get_sqlite_column(
    name: str,
    type: Literal[
        "BLOB",
        "BOOLEAN",
        "DATE",
        "DATETIME",
        "FLOAT",
        "INTEGER",
        "JSON",
        "NULL",
        "NUMERIC",
        "REAL",
        "TEXT",
        "TIMESTAMP",
        "VARCHAR",
    ],
    default: Optional[Any] = None,
    foreign_key: Optional[str] = None,
    nullable: bool = True,
    on_delete: Literal["CASCADE", "NO_ACTION", "RESTRICT", "SET_NULL"] = "NO_ACTION",
    on_update: Literal["CASCADE", "NO_ACTION", "RESTRICT", "SET_NULL"] = "NO_ACTION",
    primary_key: bool = False,
    unique: bool = False,
) -> Dict[str, Any]:
    """
    Creates a dictionary representing the definition of a database column for SQLite.

    Args:
        name (str): The name of the column.
        type (Literal): The data type of the column. Must be one of:
            "BLOB", "BOOLEAN", "DATE", "DATETIME", "FLOAT", "INTEGER",
            "JSON", "NULL", "NUMERIC", "REAL", "TEXT", "TIMESTAMP", or "VARCHAR".
        default (Optional[Any], optional): The default value for the column. Defaults to None.
        foreign_key (Optional[str], optional): A foreign key reference in the format "table(column)".
            Defaults to None, meaning no foreign key constraint.
        nullable (bool, optional): Whether this column can be NULL. Defaults to True.
        on_delete (Literal, optional): Action to perform on delete for foreign key constraint.
            One of "CASCADE", "NO_ACTION", "RESTRICT", or "SET_NULL".
            Defaults to "NO_ACTION".
        on_update (Literal, optional): Action to perform on update for foreign key constraint.
            One of "CASCADE", "NO_ACTION", "RESTRICT", or "SET_NULL".
            Defaults to "NO_ACTION".
        primary_key (bool, optional): Whether this column is a primary key. Defaults to False.
        unique (bool, optional): Whether this column has a UNIQUE constraint. Defaults to False.

    Returns:
        Dict[str, Any]: A dictionary containing all column attributes, suitable for use
        in schema generation or validation within your application.

    Notes:
        - SQLite does not natively support column comments or descriptions.
        - The `foreign_key` parameter should be specified only if a foreign key constraint is desired.
        - Default values must be compatible with the specified SQLite data type.
        - This function does not generate SQL statements, it only returns the column metadata.
    """

    return {
        "name": name,
        "type": type,
        "default": default,
        "foreign_key": foreign_key,
        "nullable": nullable,
        "on_delete": on_delete,
        "on_update": on_update,
        "primary_key": primary_key,
        "unique": unique,
    }


def get_sqlite_table(
    columns: List[Dict[str, Any]],
    name: str,
) -> Dict[str, Any]:
    """
    Creates a dictionary representing an SQLite table schema.

    Args:
        columns (List[Dict[str, Any]]): A list of column definitions, where each column is represented
            as a dictionary (e.g., as returned by `get_sqlite_column`).
        name (str): The name of the table.

    Returns:
        Dict[str, Any]: A dictionary containing the table name and its columns, structured as:
            {
                "name": str,
                "columns": List[Dict[str, Any]],
            }

    Notes:
        - This function does not execute any SQL or interact with a database; it only creates
          an in-memory representation of the table schema.
        - The resulting dictionary can be used for schema generation, validation, or further processing.
    """

    return {
        "name": name,
        "columns": columns,
    }


async def insert(
    query: str,
    params: Optional[List[Any]] = None,
) -> Optional[int]:
    """
    Executes an asynchronous SQL INSERT statement on the SQLite database.

    This function is intended for INSERT queries that add new rows to a table.
    It opens an asynchronous connection to the database, executes the query with optional parameters,
    commits the transaction, and returns the last inserted row ID.

    Args:
        query (str): The SQL INSERT query string to execute.
        params (Optional[List[Any]], optional): A list of parameters to safely substitute into the query.
            Defaults to None.

    Returns:
        Optional[int]: The row ID of the last inserted row. Returns None if the insertion failed.

    Raises:
        Exception: Any exception occurring during database connection, query execution,
        or commit will be caught and logged via the `exception` logger method.

    Notes:
        - Parameterized queries are strongly recommended to avoid SQL injection.
        - The returned row ID can be used for further operations referencing the inserted row.
    """

    try:
        # Open an asynchronous connection to the SQLite database
        async with aiosqlite.connect(database=DATABASE_PATH) as db:
            # Execute the INSERT query with the provided parameters
            cursor: aiosqlite.Cursor = await db.execute(
                parameters=params or [],
                sql=query,
            )

            # Commit the transaction to persist changes
            await db.commit()

            # Return the last inserted row ID from the cursor
            return cursor.lastrowid
    except Exception as e:
        # Log any exception that occurs during the insert operation
        exception(
            exception=e,
            message=f"Caught an exception while attempting to insert with query '{query}' and parameters {params}.",
            name="sqlite.insert",
        )

        # Return None to indicate failure
        return None


async def update(
    query: str,
    params: Optional[List[Any]] = None,
) -> Optional[int]:
    """
    Executes an asynchronous SQL UPDATE statement on the SQLite database.

    This function is intended for UPDATE queries that modify existing rows in a table.
    It opens an asynchronous connection to the database, executes the query with optional parameters,
    commits the transaction, and returns the number of rows affected.

    Args:
        query (str): The SQL UPDATE query string to execute.
        params (Optional[List[Any]], optional): A list of parameters to safely substitute into the query.
            Defaults to None.

    Returns:
        Optional[int]: The number of rows updated. Returns None if the update failed.

    Raises:
        Exception: Any exception occurring during database connection, query execution,
        or commit will be caught and logged via the `exception` logger method.

    Notes:
        - Parameterized queries are strongly recommended to avoid SQL injection.
    """

    try:
        # Create and return a connection proxy to the sqlite database.
        async with aiosqlite.connect(database=DATABASE_PATH) as db:
            # Create a cursor and execute the given query.
            cursor: aiosqlite.Cursor = await db.execute(
                parameters=params or [],
                sql=query,
            )

            # Commit the current transaction
            await db.commit()

            # Return the count of affected rows
            return cursor.rowcount
    except Exception as e:
        # Log the exception
        exception(
            exception=e,
            message=f"Caught an exception while attempting to update with query '{query}' and parameters {params}.",
            name="sqlite.update",
        )

        # Return None indiciation that an exception has occurred
        return None
