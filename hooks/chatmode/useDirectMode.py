from react import MutableRefObject, useContext
from react_hot_toast import toast
from react_i18next import useTranslation
from react_query import useMutation
from typing import Any, Dict, List

from services.useApiService import useApiService
from utils.app.clientstream import updateConversationFromStream
from utils.app.conversation import createConversationNameFromMessage
from types.chat import ChatBody, ChatModeRunner, Conversation, Message
from pages.api.home.home.context import HomeContext
from useConversations import useConversations

def useDirectMode(conversations: List[Conversation], stopConversationRef: MutableRefObject[bool]) -> ChatModeRunner:
    """
    Custom hook for using Direct mode.

    Args:
        conversations: The list of conversations.
        stopConversationRef: The mutable reference to the stop conversation flag.

    Returns:
        The chat mode runner.
    """
    { t: errT } = useTranslation('error')

    {
        dispatch: homeDispatch
    } = useContext(HomeContext)
    apiService = useApiService()
    _, conversationsAction = useConversations()

    mutation = useMutation(
        mutationFn=lambda params: apiService.chat(params),
        onMutate=lambda variables: {
            homeDispatch({ 'field': 'loading', 'value': True }),
            homeDispatch({ 'field': 'messageIsStreaming', 'value': True })
        },
        onSuccess=lambda response, variables, context: {
            data = response['body']
            {
                conversation: updatedConversation,
                message,
                selectedConversation
            } = variables
            if not data:
                homeDispatch({ 'field': 'loading', 'value': False }),
                homeDispatch({ 'field': 'messageIsStreaming', 'value': False }),
                return

            if len(updatedConversation['messages']) == 1:
                {
                    content
                } = message
                customName = createConversationNameFromMessage(content)
                updatedConversation = {
                    '...updatedConversation',
                    'name': customName
                }

            homeDispatch({ 'field': 'loading', 'value': False }),
            updatedConversation = updateConversationFromStream(
                data,
                # controller,
                new AbortController(),
                homeDispatch,
                updatedConversation,
                stopConversationRef
            )
            stopConversationRef.current = False
            updatedConversations = [
                updatedConversation if conversation['id'] == selectedConversation['id'] else conversation
                for conversation in conversations
            ]
            if len(updatedConversations) == 0:
                updatedConversations.append(updatedConversation)
            await conversationsAction.updateAll(updatedConversations)
            homeDispatch({ 'field': 'messageIsStreaming', 'value': False })
        },
        onError=lambda error: {
            console.log(error),
            homeDispatch({ 'field': 'loading', 'value': False }),
            homeDispatch({ 'field': 'messageIsStreaming', 'value': False }),
            if isinstance(error, Response):
                json = await error.json()
                toast.error(errT(json.get('error') or json.get('message') or 'error'))
            else:
                toast.error(error?.toString() or 'error')
        }
    )

    def run(params: Dict[str, Any]) -> None:
        """
        Runs the chat mode with the specified parameters.

        Args:
            params: The chat mode runner parameters.
        """
        mutation.mutate(params)

    return {
        'run': run
    }
