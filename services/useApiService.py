from typing import Dict, Any, Optional
from react import useCallback
from hooks import useFetch
from types import PlanningRequest, PlanningResponse, Plugin, PluginResult, RunPluginRequest, ChatBody, Conversation, Message

def useApiService() -> Dict[str, Any]:
    """
    Custom React hook for API service.

    Returns:
        Dict[str, Any]: API service methods.
    """

    fetchService = useFetch()

    def chat(params: Dict[str, Any], signal: Optional[AbortSignal] = None) -> Any:
        """
        Sends a chat request.

        Args:
            params (Dict[str, Any]): Request parameters.
            signal (Optional[AbortSignal], optional): AbortSignal for cancelling the request.

        Returns:
            Any: Chat response.
        """

        return fetchService.post('/api/chat', {
            'body': params['body'],
            'headers': {
                'Content-Type': 'application/json',
            },
            'signal': signal,
            'rawResponse': True,
        })

    def google_search(params: Dict[str, Any], signal: Optional[AbortSignal] = None) -> Any:
        """
        Sends a Google search request.

        Args:
            params (Dict[str, Any]): Request parameters.
            signal (Optional[AbortSignal], optional): AbortSignal for cancelling the request.

        Returns:
            Any: Google search response.
        """

        return fetchService.post('/api/google', {
            'body': params['body'],
            'headers': {
                'Content-Type': 'application/json',
            },
            'signal': signal,
            'rawResponse': True,
        })

    def planning(params: PlanningRequest, signal: Optional[AbortSignal] = None) -> PlanningResponse:
        """
        Sends a planning request.

        Args:
            params (PlanningRequest): Request parameters.
            signal (Optional[AbortSignal], optional): AbortSignal for cancelling the request.

        Returns:
            PlanningResponse: Planning response.
        """

        return fetchService.post('/api/planning', {
            'body': params,
            'headers': {
                'Content-Type': 'application/json',
            },
            'signal': signal,
        })

    def planning_conv(params: PlanningRequest, signal: Optional[AbortSignal] = None) -> PlanningResponse:
        """
        Sends a planning conversation request.

        Args:
            params (PlanningRequest): Request parameters.
            signal (Optional[AbortSignal], optional): AbortSignal for cancelling the request.

        Returns:
            PlanningResponse: Planning response.
        """

        return fetchService.post('/api/planningconv', {
            'body': params,
            'headers': {
                'Content-Type': 'application/json',
            },
            'signal': signal,
        })

    def run_plugin(params: RunPluginRequest, signal: Optional[AbortSignal] = None) -> PluginResult:
        """
        Sends a run plugin request.

        Args:
            params (RunPluginRequest): Request parameters.
            signal (Optional[AbortSignal], optional): AbortSignal for cancelling the request.

        Returns:
            PluginResult: Plugin result.
        """

        return fetchService.post('/api/runplugin', {
            'body': params,
            'headers': {
                'Content-Type': 'application/json',
            },
            'signal': signal,
        })

    def get_plugins(signal: Optional[AbortSignal] = None) -> List[Plugin]:
        """
        Sends a request to retrieve available plugins.

        Args:
            signal (Optional[AbortSignal], optional): AbortSignal for cancelling the request.

        Returns:
            List[Plugin]: List of available plugins.
        """

        return fetchService.post('/api/plugins', {
            'headers': {
                'Content-Type': 'application/json',
            },
            'signal': signal,
        })

    return {
        'chat': chat,
        'google_search': google_search,
        'planning': planning,
        'planning_conv': planning_conv,
        'run_plugin': run_plugin,
        'get_plugins': get_plugins,
    }
