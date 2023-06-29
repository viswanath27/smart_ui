from typing import Dict, Union
from starlette.requests import Request
from starlette.datastructures import Headers
from starlette.types import ASGIApp


def extract_headers(request: Union[Request, ASGIApp]) -> Dict[str, str]:
    """
    Extracts headers from a Starlette Request or ASGIApp object.

    Args:
        request (Union[Request, ASGIApp]): The Starlette Request or ASGIApp object.

    Returns:
        Dict[str, str]: A dictionary containing the extracted headers.
    """
    result = {}
    if isinstance(request, Request):
        for key, value in request.headers.items():
            result[key] = value
    else:
        headers = getattr(request, "headers", {})
        for key, value in headers.items():
            result[key] = str(value) if value is not None else ""
    return result
