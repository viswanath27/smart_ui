from typing import List

class KeyValuePair:
    """
    Represents a key-value pair.

    Attributes:
        key (str): The key of the pair.
        value (Any): The value associated with the key.
    """

    def __init__(self, key: str, value):
        self.key = key
        self.value = value

class ChatMode:
    """
    Represents a chat mode.

    Attributes:
        id (str): The ID of the chat mode.
        name (str): The name of the chat mode.
        requiredKeys (List[KeyValuePair]): The required key-value pairs for the chat mode.
    """

    def __init__(self, id: str, name: str, requiredKeys: List[KeyValuePair]):
        self.id = id
        self.name = name
        self.requiredKeys = requiredKeys

class ChatModeKey:
    """
    Represents a chat mode key.

    Attributes:
        chatModeId (str): The ID of the chat mode.
        requiredKeys (List[KeyValuePair]): The required key-value pairs for the chat mode.
    """

    def __init__(self, chatModeId: str, requiredKeys: List[KeyValuePair]):
        self.chatModeId = chatModeId
        self.requiredKeys = requiredKeys

class ChatModeID:
    DIRECT = 'direct'
    AGENT = 'agent'
    CONVERSATIONAL_AGENT = 'conversational-agent'
    GOOGLE_SEARCH = 'google-search'

class ChatModeName:
    DIRECT = 'Chat'
    AGENT = 'Agent'
    CONVERSATIONAL_AGENT = 'Conversational Agent'
    GOOGLE_SEARCH = 'Google Search'

ChatModes = {
    ChatModeID.DIRECT: ChatMode(
        id=ChatModeID.DIRECT,
        name=ChatModeName.DIRECT,
        requiredKeys=[]
    ),
    ChatModeID.AGENT: ChatMode(
        id=ChatModeID.AGENT,
        name=ChatModeName.AGENT,
        requiredKeys=[]
    ),
    ChatModeID.CONVERSATIONAL_AGENT: ChatMode(
        id=ChatModeID.CONVERSATIONAL_AGENT,
        name=ChatModeName.CONVERSATIONAL_AGENT,
        requiredKeys=[]
    ),
    ChatModeID.GOOGLE_SEARCH: ChatMode(
        id=ChatModeID.GOOGLE_SEARCH,
        name=ChatModeName.GOOGLE_SEARCH,
        requiredKeys=[
            KeyValuePair(key='GOOGLE_API_KEY', value=''),
            KeyValuePair(key='GOOGLE_CSE_ID', value=''),
        ]
    )
}

ChatModeList = list(ChatModes.values())
