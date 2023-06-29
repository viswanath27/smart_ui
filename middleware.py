from typing import Callable, Dict, Any
from fastapi import Request
from fastapi.responses import Response

def authorized(callback: Callable[[Dict[str, Any]], bool]):
    """
    Decorator for endpoint authorization.

    Args:
        callback (Callable[[Dict[str, Any]], bool]): The authorization callback function.

    Returns:
        Callable[[Callable[[Request], Response]], Callable[[Request], Response]]: Decorated endpoint function.

    """
    def decorator(endpoint: Callable[[Request], Response]):
        async def wrapper(request: Request):
            token = request.headers.get("Authorization")
            if callback({"token": token}):
                return await endpoint(request)
            else:
                return Response(status_code=401)

        return wrapper

    return decorator

@authorized
async def authorized_endpoint(request: Request):
    """
    Authorized endpoint.

    Args:
        request (Request): The incoming request.

    Returns:
        Response: The response for the authorized endpoint.

    """
    # Process the authorized request here
    pass

