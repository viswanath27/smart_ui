from typing import Any, Dict, List, Tuple
from react import useCallback, useContext
from react_i18next import useTranslation
from utils.app.const import DEFAULT_SYSTEM_PROMPT
from utils.trpc import trpc
from pages.api.home.home_context import HomeContext
from uuid import uuid4

Conversation = Dict[str, Any]
KeyValuePair = Dict[str, Any]
OpenAIModels = Dict[str, Any]

ConversationsAction = Dict[str, Any]

def useConversations() -> Tuple[List[Conversation], ConversationsAction]:
    """
    Custom hook for managing conversations.

    Returns:
        A tuple containing the conversations list and the conversations action.
    """
    t = useTranslation('chat')['t']
    tErr = useTranslation('error')['t']
    conversationUpdateAll = trpc.conversations.updateAll.useMutation()
    conversationUpdate = trpc.conversations.update.useMutation()
    conversationRemove = trpc.conversations.remove.useMutation()
    conversationRemoveAll = trpc.conversations.removeAll.useMutation()
    homeContext = useContext(HomeContext)
    defaultModelId = homeContext['state']['defaultModelId']
    conversations = homeContext['state']['conversations']
    selectedConversation = homeContext['state']['selectedConversation']
    settings = homeContext['state']['settings']
    dispatch = homeContext['dispatch']

    def updateAll(updated: List[Conversation]) -> List[Conversation]:
        """
        Updates all conversations.

        Args:
            updated: The updated conversations.

        Returns:
            The updated conversations.
        """
        conversationUpdateAll.mutateAsync(updated)
        dispatch({ 'field': 'conversations', 'value': updated })
        return updated

    def add() -> List[Conversation]:
        """
        Adds a new conversation.

        Raises:
            Error: If there is no default model.

        Returns:
            The updated conversations.
        """
        if not defaultModelId:
            raise Exception('No default model')

        lastConversation = conversations[-1] if conversations else None
        newConversation = {
            'id': uuid4(),
            'name': f"{t('New Conversation')}",
            'messages': [],
            'model': lastConversation['model'] if lastConversation else {
                'id': OpenAIModels[defaultModelId]['id'],
                'name': OpenAIModels[defaultModelId]['name'],
                'maxLength': OpenAIModels[defaultModelId]['maxLength'],
                'tokenLimit': OpenAIModels[defaultModelId]['tokenLimit']
            },
            'prompt': t(DEFAULT_SYSTEM_PROMPT),
            'temperature': settings['defaultTemperature'],
            'folderId': None
        }

        conversationUpdate.mutateAsync(newConversation)
        newState = [newConversation, *conversations]
        dispatch({ 'field': 'conversations', 'value': newState })

        dispatch({ 'field': 'selectedConversation', 'value': newConversation })
        dispatch({ 'field': 'loading', 'value': False })
        return newState

    def update(conversation: Conversation) -> Conversation:
        """
        Updates a conversation.

        Args:
            conversation: The conversation to update.

        Returns:
            The updated conversation.
        """
        newConversations = [conversation if f['id'] == conversation['id'] else f for f in conversations]
        conversationUpdate.mutateAsync(conversation)
        dispatch({ 'field': 'conversations', 'value': newConversations })
        if selectedConversation and selectedConversation['id'] == conversation['id']:
            dispatch({ 'field': 'selectedConversation', 'value': conversation })
        return conversation

    def updateValue(conversation: Conversation, kv: KeyValuePair) -> Conversation:
        """
        Updates a conversation value.

        Args:
            conversation: Theconversation to update.
            kv: The key-value pair to update.

        Returns:
            The updated conversation.
        """
        updatedConversation = { **conversation, kv['key']: kv['value'] }
        newState = update(updatedConversation)
        if selectedConversation and selectedConversation['id'] == conversation['id']:
            dispatch({ 'field': 'selectedConversation', 'value': updatedConversation })
        return newState

    def remove(conversation: Conversation) -> List[Conversation]:
        """
        Removes a conversation.

        Args:
            conversation: The conversation to remove.

        Returns:
            The updated conversations.
        """
        conversationRemove.mutateAsync({ 'id': conversation['id'] })
        updatedConversations = [c for c in conversations if c['id'] != conversation['id']]
        dispatch({ 'field': 'conversations', 'value': updatedConversations })
        return updatedConversations

    def clear() -> List[Conversation]:
        """
        Clears all conversations.

        Returns:
            An empty list.
        """
        conversationRemoveAll.mutateAsync()
        dispatch({ 'field': 'conversations', 'value': [] })
        return []

    return conversations, {
        'add': add,
        'update': update,
        'updateValue': updateValue,
        'updateAll': updateAll,
        'remove': remove,
        'clear': clear
    }
