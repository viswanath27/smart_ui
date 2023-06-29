from typing import Optional, List
import React
from react_i18next import useTranslation
from types.agent import Plugin
from types.chat import ChatBody, Conversation, Message
from types.chatmode import ChatMode
from pages.api.home.home_context import HomeContext
from .chatmode.useChatModeRunner import useChatModeRunner
from .useConversations import useConversations

def useMesseageSender():
    """
    Custom hook for sending messages.

    Returns:
        A function that sends a message and triggers the chat mode runner.
    """
    homeContext = useContext(HomeContext)
    selectedConversation = homeContext['state']['selectedConversation']
    apiKey = homeContext['state']['apiKey']
    conversations, _ = useConversations()
    chatModeSelector = useChatModeRunner(conversations)

    async def sendMessage(
        message: Message,
        deleteCount: int = 0,
        chatMode: Optional[ChatMode] = None,
        plugins: List[Plugin] = []
    ):
        """
        Sends a message and triggers the chat mode runner.

        Args:
            message: The message to be sent.
            deleteCount: The number of messages to be deleted.
            chatMode: The chat mode to be used.
            plugins: The list of plugins.

        Returns:
            None.
        """
        if not selectedConversation:
            return

        conversation = selectedConversation
        if deleteCount:
            updatedMessages = conversation['messages'][:-deleteCount]
            updatedConversation = {
                **conversation,
                'messages': updatedMessages + [message]
            }
        else:
            updatedConversation = {
                **conversation,
                'messages': conversation['messages'] + [message]
            }
        
        chatBody: ChatBody = {
            'model': updatedConversation['model'],
            'messages': updatedConversation['messages'],
            'key': apiKey,
            'prompt': conversation['prompt'],
            'temperature': conversation['temperature']
        }

        chatModeRunner = chatModeSelector(chatMode)
        chatModeRunner.run({
            'body': chatBody,
            'conversation': updatedConversation,
            'message': message,
            'selectedConversation': selectedConversation,
            'plugins': plugins
        })

    return sendMessage

