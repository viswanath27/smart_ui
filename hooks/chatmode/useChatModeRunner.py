from react import MutableRefObject, useContext
from hooks.chatmode.useAgentMode import useAgentMode
from hooks.chatmode.useDirectMode import useDirectMode
from hooks.chatmode.useGoogleMode import useGoogleMode
from types.chat import ChatModeRunner, Conversation
from types.chatmode import ChatMode, ChatModeID
from pages.api.home.home.context import HomeContext

def useChatModeRunner(conversations: List[Conversation]) -> ChatModeRunner:
    """
    Custom hook for using the chat mode runner.

    Args:
        conversations: The list of conversations.

    Returns:
        The chat mode runner.
    """
    {
        state: { stopConversationRef }
    } = useContext(HomeContext)
    directMode = useDirectMode(conversations, stopConversationRef)
    googleMode = useGoogleMode(conversations)
    conversationalAgentMode = useAgentMode(conversations, stopConversationRef, True)
    agentMode = useAgentMode(conversations, stopConversationRef, False)

    def chatModeRunner(plugin: Optional[ChatMode]) -> ChatModeRunner:
        """
        Returns the chat mode runner based on the specified plugin.

        Args:
            plugin: The chat mode plugin.

        Returns:
            The chat mode runner.
        """
        if not plugin:
            return directMode

        if plugin['id'] == ChatModeID.GOOGLE_SEARCH:
            return googleMode
        elif plugin['id'] == ChatModeID.AGENT:
            return agentMode
        elif plugin['id'] == ChatModeID.CONVERSATIONAL_AGENT:
            return conversationalAgentMode
        else:
            return directMode

    return chatModeRunner
