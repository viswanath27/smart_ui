import json
from typing import Any, Dict, Optional
from fetch import fetch

RequestModel = Dict[str, Any]
RequestWithBodyModel = Dict[str, Any]

def useFetch():
    """
    Custom hook for making HTTP requests.

    Returns:
        A dictionary with functions for different HTTP methods.
    """
    async def handleFetch(
        url: str,
        request: Optional[Any],
        signal: Optional[AbortSignal] = None,
        rawResponse: Optional[bool] = False
    ) -> Any:
        """
        Handles the HTTP fetch request.

        Args:
            url: The URL to fetch.
            request: The request model.
            signal: The AbortSignal.
            rawResponse: Flag indicating whether to return the raw response.

        Returns:
            The fetch response.
        """
        requestUrl = f"{url}{request['params']}" if request and 'params' in request else url

        requestBody = request['body'] if request and 'body' in request else request
        if request and 'body' in request:
            if isinstance(request['body'], FormData):
                requestBody = { **request, 'body': request['body'] }
            else:
                requestBody = { **request, 'body': json.dumps(request['body']) }

        headers = {
            **(request['headers'] if request and 'headers' in request else {}),
            **(request['body'] if request and 'body' in request and isinstance(request['body'], FormData) else { 'Content-type': 'application/json' })
        }

        response = await fetch(requestUrl, { **requestBody, 'headers': headers, 'signal': signal })

        if not response.ok:
            raise response

        if rawResponse:
            return response

        contentType = response.headers.get('content-type')
        contentDisposition = response.headers.get('content-disposition')

        headers = response.headers

        if contentType:
            if 'application/json' in contentType or 'text/plain' in contentType:
                result = response.json()
            elif 'attachment' in contentDisposition:
                result = response.blob()
            else:
                result = response
        else:
            result = response

        return result

    return {
        'get': lambda url, request=None: handleFetch(url, { **request, 'method': 'get' }),
        'post': lambda url, request=None: handleFetch(url, { **request, 'method': 'post' }, request['signal'] if request and 'signal' in request else None, request['rawResponse'] if request and 'rawResponse' in request else None),
        'put': lambda url, request=None: handleFetch(url, { **request, 'method': 'put' }),
        'patch': lambda url, request=None: handleFetch(url, { **request, 'method': 'patch' }),
        'delete': lambda url, request=None: handleFetch(url, { **request, 'method': 'delete' })
    }
