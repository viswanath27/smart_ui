from typing import List, Optional

class Conversation:
    """
    Represents a conversation in the chat.
    """

    # Conversation implementation goes here
    pass

class FolderInterface:
    """
    Represents a folder in the chat.
    """

    # FolderInterface implementation goes here
    pass

class Prompt:
    """
    Represents a prompt in the chat.
    """

    # Prompt implementation goes here
    pass

class LocalStorage:
    """
    Represents the schema for the local storage.
    """

    apiKey: str
    conversationHistory: List[Conversation]
    selectedConversation: Conversation
    theme: str
    folders: List[FolderInterface]
    prompts: List[Prompt]
    showChatbar: bool
    showPromptbar: bool
    pluginKeys: List[str]

    def __init__(
        self,
        apiKey: str,
        conversationHistory: List[Conversation],
        selectedConversation: Conversation,
        theme: str,
        folders: List[FolderInterface],
        prompts: List[Prompt],
        showChatbar: bool,
        showPromptbar: bool,
        pluginKeys: List[str]
    ):
        self.apiKey = apiKey
        self.conversationHistory = conversationHistory
        self.selectedConversation = selectedConversation
        self.theme = theme
        self.folders = folders
        self.prompts = prompts
        self.showChatbar = showChatbar
        self.showPromptbar = showPromptbar
        self.pluginKeys = pluginKeys

