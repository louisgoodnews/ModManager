"""
Author: Louis Goodnews
Date: 2025-08-10
"""

import aiohttp
import asyncio

from typing import Any, Dict, Final, List, Optional, Union

from utils.logging import exception


__all__: Final[List[str]] = [
    "http_delete",
    "http_get",
    "http_head",
    "http_options",
    "http_patch",
    "http_post",
    "http_put",
]


async def __handle_reponse_type__(
    response: aiohttp.ClientResponse,
) -> Union[
    bytes,
    Dict[str, Any],
    str,
]:
    """
    Parses the body of an aiohttp.ClientResponse based on its Content-Type.

    This asynchronous function inspects the Content-Type header of the HTTP response
    and returns the response body parsed accordingly:
    - If the content type is JSON (`application/json`), it returns the parsed JSON as a dictionary.
    - If the content type indicates text (e.g., `text/plain`, `text/html`), it returns the response as a string.
    - For all other content types, it returns the raw bytes of the response.

    Args:
        response (aiohttp.ClientResponse): The HTTP response object from an aiohttp request.

    Returns:
        Union[bytes, Dict[str, Any], str]: The parsed response content, which may be:
            - A dictionary if the response contains JSON,
            - A string if the response contains text,
            - Raw bytes otherwise.

    Raises:
        aiohttp.ClientError: If reading the response content fails.
    """

    content_type: str = response.content_type.lower()

    if "application/json" in content_type:
        return await response.json(encoding="utf-8")
    elif "text/" in content_type:
        return await response.text(encoding="utf-8")
    else:
        return await response.read()


def http_delete(
    url: str,
    headers: Dict[str, Any] = None,
    *args,
    **kwargs,
) -> Dict[str, Any]:
    """
    Synchronous wrapper for an asynchronous HTTP DELETE request.

    This function runs an asynchronous DELETE request internally using aiohttp and
    returns the response data as a dictionary. It is designed to be called
    synchronously from non-async code.

    Args:
        url (str): The target URL for the DELETE request.
        headers (Dict[str, Any], optional): Optional HTTP headers to include in the request.
        *args: Additional positional arguments passed to the underlying aiohttp DELETE call.
        **kwargs: Additional keyword arguments passed to the underlying aiohttp DELETE call.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - "body": Parsed response content (JSON dict, text string, or raw bytes).
            - "content_type": The Content-Type header of the response.
            - "method": The HTTP method used ("DELETE").
            - "reason": The HTTP reason phrase.
            - "status": The HTTP status code.
            - "url": The requested URL as a string.

        Returns an empty dictionary if an error occurs during the request.
    """

    async def __delete__(
        url: str,
        headers: Dict[str, Any],
        *args,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Performs an asynchronous HTTP DELETE request to the specified URL using aiohttp.

        This coroutine creates a new aiohttp ClientSession, sends a DELETE request with optional headers
        and additional parameters, and processes the response. It handles HTTP errors by raising
        exceptions and logs any exceptions that occur during the request.

        Args:
            url (str): The target URL for the DELETE request.
            headers (Dict[str, Any]): Optional HTTP headers to include in the request.
            *args: Additional positional arguments passed to aiohttp.ClientSession.delete().
            **kwargs: Additional keyword arguments passed to aiohttp.ClientSession.delete().

        Returns:
            Dict[str, Any]: A dictionary containing the following keys:
                - "body": The parsed response content (JSON dict, text string, or raw bytes).
                - "content_type": The Content-Type header of the response.
                - "method": The HTTP method used ("DELETE").
                - "reason": The HTTP reason phrase.
                - "status": The HTTP status code.
                - "url": The requested URL as a string.

            Returns an empty dictionary if an exception occurs during the request.

        Raises:
            aiohttp.ClientResponseError: If the HTTP response status indicates an error.
        """

        try:
            async with aiohttp.ClientSession() as session:
                async with session.delete(
                    url,
                    headers=headers,
                    *args,
                    **kwargs,
                ) as response:
                    response.raise_for_status()

                    return {
                        "body": await __handle_reponse_type__(response=response),
                        "content_type": response.content_type,
                        "method": "DELETE",
                        "reason": response.reason,
                        "status": response.status,
                        "url": str(response.url),
                    }
        except Exception as e:
            exception(
                exception=e,
                message="Caught an exception while attempting run 'DELETE' request",
                name="http.delete",
            )
            return {}

    return asyncio.run(
        __delete__(
            headers=headers or {},
            url=url,
            *args,
            **kwargs,
        )
    )


def http_get(
    url: str,
    headers: Optional[Dict[str, Any]] = None,
    *args,
    **kwargs,
) -> Dict[str, Any]:
    """
    Synchronous wrapper for an asynchronous HTTP GET request.

    This function runs an asynchronous GET request internally using aiohttp and
    returns the response data as a dictionary. It is designed to be called
    synchronously from non-async code.

    Args:
        url (str): The target URL for the GET request.
        headers (Dict[str, Any], optional): Optional HTTP headers to include in the request.
        *args: Additional positional arguments passed to the underlying aiohttp GET call.
        **kwargs: Additional keyword arguments passed to the underlying aiohttp GET call.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - "body": Parsed response content (JSON dict, text string, or raw bytes).
            - "content_type": The Content-Type header of the response.
            - "method": The HTTP method used ("GET").
            - "reason": The HTTP reason phrase.
            - "status": The HTTP status code.
            - "url": The requested URL as a string.

        Returns an empty dictionary if an error occurs during the request.
    """

    async def __get__(
        url: str,
        headers: Optional[Dict[str, Any]] = None,
        *args,
        **kwargs,
    ) -> None:
        """
        Performs an asynchronous HTTP GET request to the specified URL using aiohttp.

        This coroutine creates a new aiohttp ClientSession, sends a GET request with optional headers
        and additional parameters, and processes the response. It handles HTTP errors by raising
        exceptions and logs any exceptions that occur during the request.

        Args:
            url (str): The target URL for the GET request.
            headers (Dict[str, Any], optional): Optional HTTP headers to include in the request.
            *args: Additional positional arguments passed to aiohttp.ClientSession.get().
            **kwargs: Additional keyword arguments passed to aiohttp.ClientSession.get().

        Returns:
            Dict[str, Any]: A dictionary containing the following keys:
                - "body": The parsed response content (JSON dict, text string, or raw bytes).
                - "content_type": The Content-Type header of the response.
                - "method": The HTTP method used ("GET").
                - "reason": The HTTP reason phrase.
                - "status": The HTTP status code.
                - "url": The requested URL as a string.

            Returns an empty dictionary if an exception occurs during the request.

        Raises:
            aiohttp.ClientResponseError: If the HTTP response status indicates an error.
        """

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    headers=headers,
                    url=url,
                    *args,
                    **kwargs,
                ) as response:
                    #
                    response.raise_for_status()

                    return {
                        "body": await __handle_reponse_type__(response=response),
                        "content_type": response.content_type,
                        "method": "GET",
                        "reason": response.reason,
                        "status": response.status,
                        "url": str(response.url),
                    }
        except Exception as e:
            exception(
                exception=e,
                message="Caught an exception while attempting run 'GET' request",
                name="http.get",
            )

    return asyncio.run(
        __get__(
            headers=headers,
            url=url,
            *args,
            **kwargs,
        )
    )


def http_head(
    url: str,
    headers: Dict[str, Any] = None,
    *args,
    **kwargs,
) -> Dict[str, Any]:
    """
    Synchronous wrapper for an asynchronous HTTP HEAD request.

    This function runs an asynchronous HEAD request internally using aiohttp and
    returns the response metadata as a dictionary. It is designed to be called
    synchronously from non-async code.

    Args:
        url (str): The target URL for the HEAD request.
        headers (Dict[str, Any], optional): Optional HTTP headers to include in the request.
        *args: Additional positional arguments passed to the underlying aiohttp HEAD call.
        **kwargs: Additional keyword arguments passed to the underlying aiohttp HEAD call.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - "content_type": The Content-Type header of the response.
            - "method": The HTTP method used ("HEAD").
            - "reason": The HTTP reason phrase.
            - "status": The HTTP status code.
            - "url": The requested URL as a string.

        Returns an empty dictionary if an error occurs during the request.
    """

    async def __head__(
        url: str,
        headers: Dict[str, Any],
        *args,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Performs an asynchronous HTTP HEAD request to the specified URL using aiohttp.

        This coroutine creates a new aiohttp ClientSession, sends a HEAD request with optional headers
        and additional parameters, and processes the response. It handles HTTP errors by raising
        exceptions and logs any exceptions that occur during the request.

        Args:
            url (str): The target URL for the HEAD request.
            headers (Dict[str, Any]): Optional HTTP headers to include in the request.
            *args: Additional positional arguments passed to aiohttp.ClientSession.head().
            **kwargs: Additional keyword arguments passed to aiohttp.ClientSession.head().

        Returns:
            Dict[str, Any]: A dictionary containing the following keys:
                - "content_type": The Content-Type header of the response.
                - "method": The HTTP method used ("HEAD").
                - "reason": The HTTP reason phrase.
                - "status": The HTTP status code.
                - "url": The requested URL as a string.

            Returns an empty dictionary if an exception occurs during the request.

        Raises:
            aiohttp.ClientResponseError: If the HTTP response status indicates an error.
        """

        try:
            async with aiohttp.ClientSession() as session:
                async with session.head(
                    url,
                    headers=headers,
                    *args,
                    **kwargs,
                ) as response:
                    response.raise_for_status()

                    return {
                        "content_type": response.content_type,
                        "method": "HEAD",
                        "reason": response.reason,
                        "status": response.status,
                        "url": str(response.url),
                    }
        except Exception as e:
            exception(
                exception=e,
                message="Caught an exception while attempting run 'HEAD' request",
                name="http.head",
            )
            return {}

    return asyncio.run(
        __head__(
            headers=headers or {},
            url=url,
            *args,
            **kwargs,
        )
    )


def http_options(
    url: str,
    headers: Dict[str, Any] = None,
    *args,
    **kwargs,
) -> Dict[str, Any]:
    """
    Synchronous wrapper for an asynchronous HTTP OPTIONS request.

    This function runs an asynchronous OPTIONS request internally using aiohttp and
    returns the response data as a dictionary. It is designed to be called
    synchronously from non-async code.

    Args:
        url (str): The target URL for the OPTIONS request.
        headers (Dict[str, Any], optional): Optional HTTP headers to include in the request.
        *args: Additional positional arguments passed to the underlying aiohttp OPTIONS call.
        **kwargs: Additional keyword arguments passed to the underlying aiohttp OPTIONS call.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - "body": Parsed response content (JSON dict, text string, or raw bytes).
            - "content_type": The Content-Type header of the response.
            - "method": The HTTP method used ("OPTIONS").
            - "reason": The HTTP reason phrase.
            - "status": The HTTP status code.
            - "url": The requested URL as a string.

        Returns an empty dictionary if an error occurs during the request.
    """

    async def __options__(
        url: str,
        headers: Dict[str, Any],
        *args,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Performs an asynchronous HTTP OPTIONS request to the specified URL using aiohttp.

        This coroutine creates a new aiohttp ClientSession, sends an OPTIONS request with optional headers
        and additional parameters, and processes the response. It handles HTTP errors by raising
        exceptions and logs any exceptions that occur during the request.

        Args:
            url (str): The target URL for the OPTIONS request.
            headers (Dict[str, Any]): Optional HTTP headers to include in the request.
            *args: Additional positional arguments passed to aiohttp.ClientSession.options().
            **kwargs: Additional keyword arguments passed to aiohttp.ClientSession.options().

        Returns:
            Dict[str, Any]: A dictionary containing the following keys:
                - "body": The parsed response content (JSON dict, text string, or raw bytes).
                - "content_type": The Content-Type header of the response.
                - "method": The HTTP method used ("OPTIONS").
                - "reason": The HTTP reason phrase.
                - "status": The HTTP status code.
                - "url": The requested URL as a string.

            Returns an empty dictionary if an exception occurs during the request.

        Raises:
            aiohttp.ClientResponseError: If the HTTP response status indicates an error.
        """

        try:
            async with aiohttp.ClientSession() as session:
                async with session.options(
                    url,
                    headers=headers,
                    *args,
                    **kwargs,
                ) as response:
                    response.raise_for_status()

                    return {
                        "body": await __handle_reponse_type__(response=response),
                        "content_type": response.content_type,
                        "method": "OPTIONS",
                        "reason": response.reason,
                        "status": response.status,
                        "url": str(response.url),
                    }
        except Exception as e:
            exception(
                exception=e,
                message="Caught an exception while attempting run 'OPTIONS' request",
                name="http.options",
            )
            return {}

    return asyncio.run(
        __options__(
            headers=headers or {},
            url=url,
            *args,
            **kwargs,
        )
    )


def http_patch(
    url: str,
    headers: Dict[str, Any] = None,
    data: Any = None,
    *args,
    **kwargs,
) -> Dict[str, Any]:
    """
    Synchronous wrapper for an asynchronous HTTP PATCH request.

    This function runs an asynchronous PATCH request internally using aiohttp and
    returns the response data as a dictionary. It is designed to be called
    synchronously from non-async code.

    Args:
        url (str): The target URL for the PATCH request.
        headers (Dict[str, Any], optional): Optional HTTP headers to include in the request.
        data (Any, optional): The data to send in the PATCH request body.
        *args: Additional positional arguments passed to the underlying aiohttp PATCH call.
        **kwargs: Additional keyword arguments passed to the underlying aiohttp PATCH call.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - "body": Parsed response content (JSON dict, text string, or raw bytes).
            - "content_type": The Content-Type header of the response.
            - "method": The HTTP method used ("PATCH").
            - "reason": The HTTP reason phrase.
            - "status": The HTTP status code.
            - "url": The requested URL as a string.

        Returns an empty dictionary if an error occurs during the request.
    """

    async def __patch__(
        url: str,
        headers: Dict[str, Any],
        data: Any,
        *args,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Performs an asynchronous HTTP PATCH request to the specified URL using aiohttp.

        This coroutine creates a new aiohttp ClientSession, sends a PATCH request with optional headers
        and data, and processes the response. It handles HTTP errors by raising
        exceptions and logs any exceptions that occur during the request.

        Args:
            url (str): The target URL for the PATCH request.
            headers (Dict[str, Any]): Optional HTTP headers to include in the request.
            data (Any): The data to send in the PATCH request body.
            *args: Additional positional arguments passed to aiohttp.ClientSession.patch().
            **kwargs: Additional keyword arguments passed to aiohttp.ClientSession.patch().

        Returns:
            Dict[str, Any]: A dictionary containing the following keys:
                - "body": The parsed response content (JSON dict, text string, or raw bytes).
                - "content_type": The Content-Type header of the response.
                - "method": The HTTP method used ("PATCH").
                - "reason": The HTTP reason phrase.
                - "status": The HTTP status code.
                - "url": The requested URL as a string.

            Returns an empty dictionary if an exception occurs during the request.

        Raises:
            aiohttp.ClientResponseError: If the HTTP response status indicates an error.
        """

        try:
            async with aiohttp.ClientSession() as session:
                async with session.patch(
                    url,
                    headers=headers,
                    data=data,
                    *args,
                    **kwargs,
                ) as response:
                    response.raise_for_status()

                    return {
                        "body": await __handle_reponse_type__(response=response),
                        "content_type": response.content_type,
                        "method": "PATCH",
                        "reason": response.reason,
                        "status": response.status,
                        "url": str(response.url),
                    }
        except Exception as e:
            exception(
                exception=e,
                message="Caught an exception while attempting run 'PATCH' request",
                name="http.patch",
            )
            return {}

    return asyncio.run(
        __patch__(
            data=data,
            headers=headers or {},
            url=url,
            *args,
            **kwargs,
        )
    )


def http_post(
    url: str,
    headers: Dict[str, Any] = None,
    data: Any = None,
    *args,
    **kwargs,
) -> Dict[str, Any]:
    """
    Synchronous wrapper for an asynchronous HTTP POST request.

    This function runs an asynchronous POST request internally using aiohttp and
    returns the response data as a dictionary. It is designed to be called
    synchronously from non-async code.

    Args:
        url (str): The target URL for the POST request.
        headers (Dict[str, Any], optional): Optional HTTP headers to include in the request.
        data (Any, optional): The data to send in the POST request body.
        *args: Additional positional arguments passed to the underlying aiohttp POST call.
        **kwargs: Additional keyword arguments passed to the underlying aiohttp POST call.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - "body": Parsed response content (JSON dict, text string, or raw bytes).
            - "content_type": The Content-Type header of the response.
            - "method": The HTTP method used ("POST").
            - "reason": The HTTP reason phrase.
            - "status": The HTTP status code.
            - "url": The requested URL as a string.

        Returns an empty dictionary if an error occurs during the request.
    """

    async def __post__(
        url: str,
        headers: Dict[str, Any],
        data: Any,
        *args,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Performs an asynchronous HTTP POST request to the specified URL using aiohttp.

        This coroutine creates a new aiohttp ClientSession, sends a POST request with optional headers
        and data, and processes the response. It handles HTTP errors by raising
        exceptions and logs any exceptions that occur during the request.

        Args:
            url (str): The target URL for the POST request.
            headers (Dict[str, Any]): Optional HTTP headers to include in the request.
            data (Any): The data to send in the POST request body.
            *args: Additional positional arguments passed to aiohttp.ClientSession.post().
            **kwargs: Additional keyword arguments passed to aiohttp.ClientSession.post().

        Returns:
            Dict[str, Any]: A dictionary containing the following keys:
                - "body": The parsed response content (JSON dict, text string, or raw bytes).
                - "content_type": The Content-Type header of the response.
                - "method": The HTTP method used ("POST").
                - "reason": The HTTP reason phrase.
                - "status": The HTTP status code.
                - "url": The requested URL as a string.

            Returns an empty dictionary if an exception occurs during the request.

        Raises:
            aiohttp.ClientResponseError: If the HTTP response status indicates an error.
        """

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    headers=headers,
                    data=data,
                    *args,
                    **kwargs,
                ) as response:
                    response.raise_for_status()

                    return {
                        "body": await __handle_reponse_type__(response=response),
                        "content_type": response.content_type,
                        "method": "POST",
                        "reason": response.reason,
                        "status": response.status,
                        "url": str(response.url),
                    }
        except Exception as e:
            exception(
                exception=e,
                message="Caught an exception while attempting run 'POST' request",
                name="http.post",
            )
            return {}

    return asyncio.run(
        __post__(
            data=data,
            headers=headers or {},
            url=url,
            *args,
            **kwargs,
        )
    )


def http_put(
    url: str,
    headers: Dict[str, Any] = None,
    data: Any = None,
    *args,
    **kwargs,
) -> Dict[str, Any]:
    """
    Synchronous wrapper for an asynchronous HTTP PUT request.

    This function runs an asynchronous PUT request internally using aiohttp and
    returns the response data as a dictionary. It is designed to be called
    synchronously from non-async code.

    Args:
        url (str): The target URL for the PUT request.
        headers (Dict[str, Any], optional): Optional HTTP headers to include in the request.
        data (Any, optional): The data to send in the PUT request body.
        *args: Additional positional arguments passed to the underlying aiohttp PUT call.
        **kwargs: Additional keyword arguments passed to the underlying aiohttp PUT call.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - "body": Parsed response content (JSON dict, text string, or raw bytes).
            - "content_type": The Content-Type header of the response.
            - "method": The HTTP method used ("PUT").
            - "reason": The HTTP reason phrase.
            - "status": The HTTP status code.
            - "url": The requested URL as a string.

        Returns an empty dictionary if an error occurs during the request.
    """

    async def __put__(
        url: str,
        headers: Dict[str, Any],
        data: Any,
        *args,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Performs an asynchronous HTTP PUT request to the specified URL using aiohttp.

        This coroutine creates a new aiohttp ClientSession, sends a PUT request with optional headers
        and data, and processes the response. It handles HTTP errors by raising
        exceptions and logs any exceptions that occur during the request.

        Args:
            url (str): The target URL for the PUT request.
            headers (Dict[str, Any]): Optional HTTP headers to include in the request.
            data (Any): The data to send in the PUT request body.
            *args: Additional positional arguments passed to aiohttp.ClientSession.put().
            **kwargs: Additional keyword arguments passed to aiohttp.ClientSession.put().

        Returns:
            Dict[str, Any]: A dictionary containing the following keys:
                - "body": The parsed response content (JSON dict, text string, or raw bytes).
                - "content_type": The Content-Type header of the response.
                - "method": The HTTP method used ("PUT").
                - "reason": The HTTP reason phrase.
                - "status": The HTTP status code.
                - "url": The requested URL as a string.

            Returns an empty dictionary if an exception occurs during the request.

        Raises:
            aiohttp.ClientResponseError: If the HTTP response status indicates an error.
        """

        try:
            async with aiohttp.ClientSession() as session:
                async with session.put(
                    url,
                    headers=headers,
                    data=data,
                    *args,
                    **kwargs,
                ) as response:
                    response.raise_for_status()

                    return {
                        "body": await __handle_reponse_type__(response=response),
                        "content_type": response.content_type,
                        "method": "PUT",
                        "reason": response.reason,
                        "status": response.status,
                        "url": str(response.url),
                    }
        except Exception as e:
            exception(
                exception=e,
                message="Caught an exception while attempting run 'PUT' request",
                name="http.put",
            )
            return {}

    return asyncio.run(
        __put__(
            data=data,
            headers=headers or {},
            url=url,
            *args,
            **kwargs,
        )
    )
