from react import useContext
from react_hot_toast import toast
from react_i18next import useTranslation
from react_query import useMutation
from typing import Any, Dict, List

from services.useApiService import useApiService
from utils.app.homeUpdater import HomeUpdater
from types.chat import ChatModeRunner, ChatModeRunnerParams, Conversation
from pages.api.home.home.context import HomeContext
from useConversations import useConversations

def useGoogleMode(conversations: List[Conversation]) -> ChatModeRunner:
    """
    Custom hook for using Google mode.

    Args:
        conversations: The list of conversations.

    Returns:
        The chat mode runner.
    """
    { t: errT } = useTranslation('error')
    {
        state: { chatModeKeys },
        dispatch: homeDispatch
    } = useContext(HomeContext)
    apiService = useApiService()
    _, conversationsAction = useConversations()
    updater = HomeUpdater(homeDispatch)
    mutation = useMutation(
        mutationFn=lambda params: apiService.googleSearch(params),
        onMutate=lambda variables: {
            variables['body']['googleAPIKey']: next(
                (key['value'] for key in chatModeKeys
                    if key['chatModeId'] == 'google-search' and key['key'] == 'GOOGLE_API_KEY'), None
            ),
            variables['body']['googleCSEId']: next(
                (key['value'] for key in chatModeKeys
                    if key['chatModeId'] == 'google-search' and key['key'] == 'GOOGLE_CSE_ID'), None
            ),
            homeDispatch({ 'field': 'selectedConversation', 'value': variables['conversation'] }),
            homeDispatch({ 'field': 'loading', 'value': True }),
            homeDispatch({ 'field': 'messageIsStreaming', 'value': True })
        },
        onSuccess=lambda response, variables, context: {
            updatedConversation, selectedConversation = variables['conversation']
            answer = await response.json()
            updatedConversation = updater.addMessage(updatedConversation, {
                'role': 'assistant',
                'content': answer
            })
            updatedConversations = [
                updatedConversation if conversation['id'] == selectedConversation['id'] else conversation
                for conversation in conversations
            ]
            if len(updatedConversations) == 0:
                updatedConversations.append(updatedConversation)
            await conversationsAction.updateAll(updatedConversations)
            homeDispatch({ 'field': 'loading', 'value': False }),
            homeDispatch({ 'field': 'messageIsStreaming', 'value': False })
        },
        onError=lambda error: {
            homeDispatch({ 'field': 'loading', 'value': False }),
            homeDispatch({ 'field': 'messageIsStreaming', 'value': False }),
            if isinstance(error, Response):
                json = await error.json()
                toast.error(errT(json.get('error') or json.get('message') or 'error'))
            else:
                toast.error(error?.toString() or 'error')
        }
    )

    def run(params: ChatModeRunnerParams) -> None:
        """
        Runs the chat mode with the specified parameters.

        Args:
            params: The chat mode runner parameters.
        """
        mutation.mutate(params)

    return {
        'run': run
    }
