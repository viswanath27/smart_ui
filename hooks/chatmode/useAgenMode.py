from react import MutableRefObject, useContext
from react_hot_toast import toast
from react_i18next import useTranslation
from react_query import useMutation

from services.useApiService import useApiService

from utils.app.api import watchRefToAbort
from utils.app.conversation import createConversationNameFromMessage
from utils.app.homeUpdater import HomeUpdater

from types.agent import Answer, PlanningResponse, PluginResult
from types.chat import ChatModeRunner, ChatModeRunnerParams, Conversation

from pages.api.home.home.context import HomeContext

from useConversations import useConversations

def useAgentMode(conversations: List[Conversation], stopConversationRef: MutableRefObject[bool], conversational: bool) -> ChatModeRunner:
    """
    Custom hook for using the agent mode in the chat.

    Args:
        conversations: The list of conversations.
        stopConversationRef: The mutable reference object to stop the conversation.
        conversational: A boolean indicating if the mode is conversational.

    Returns:
        The chat mode runner for the agent mode.
    """
    { t } = useTranslation('chat')
    { t: errT } = useTranslation('error')

    { dispatch: homeDispatch } = useContext(HomeContext)
    apiService = useApiService()
    [_, conversationsAction] = useConversations()

    updater = HomeUpdater(homeDispatch)
    mutation = useMutation()

    def run(params: ChatModeRunnerParams):
        """
        Runs the agent mode.

        Args:
            params: The parameters for the chat mode runner.

        Returns:
            None.
        """
        mutation.mutate(params)

    def onMutate(variables):
        """
        Callback function when the mutation is initiated.

        Args:
            variables: The variables for the mutation.

        Returns:
            None.
        """
        conversation = variables['conversation']
        if len(conversation['messages']) == 1:
            conversation['name'] = createConversationNameFromMessage(variables['message']['content'])
        homeDispatch({ 'field': 'selectedConversation', 'value': conversation })
        homeDispatch({ 'field': 'loading', 'value': True })
        homeDispatch({ 'field': 'messageIsStreaming', 'value': True })

    async def onSuccess(answer: Answer, variables, context):
        """
        Callback function when the mutation is successful.

        Args:
            answer: The answer received from the mutation.
            variables: The variables for the mutation.
            context: The context for the mutation.

        Returns:
            None.
        """
        updatedConversation = updater.addMessage(variables['conversation'], { 'role': 'assistant', 'content': answer['answer'] })
        updatedConversations = [updatedConversation if conversation['id'] == variables['selectedConversation']['id'] else conversation for conversation in conversations]
        if len(updatedConversations) == 0:
            updatedConversations.append(updatedConversation)
        await conversationsAction.updateAll(updatedConversations)
        homeDispatch({ 'field': 'loading', 'value': False })
        homeDispatch({ 'field': 'messageIsStreaming', 'value': False })

    async def onError(error):
        """
        Callback function when the mutation encounters an error.

        Args:
            error: The error received from the mutation.

        Returns:
            None.
        """
        homeDispatch({ 'field': 'loading', 'value': False })
        homeDispatch({ 'field': 'messageIsStreaming', 'value': False })
        if isinstance(error, DOMException) and error['name'] == 'AbortError':
            toast.error(t('Conversation stopped'))
        elif isinstance(error, Response):
            json = await error.json()
            toast.error(errT(json['error'] or json['message'] or 'error```
        else:
            toast.error(error or 'error')

    return {
        'run': run,
        'onMutate': onMutate,
        'onSuccess': onSuccess,
        'onError': onError
    }
