from typing import List

import React
from react_query import useQuery

from services.useApiService import useApiService
from types.agent import Plugin

def usePlugins() -> dict[str, any]:
    """
    Custom hook for retrieving plugins.

    Returns:
        A dictionary containing the list of plugins and any errors.
    """
    apiService = useApiService()
    result = useQuery('plugins', apiService.getPlugins, {
        'enabled': True,
        'refetchOnMount': False,
        'refetchOnWindowFocus': False
    })
    return {
        'plugins': result['data'],
        'error': result['error']
    }
