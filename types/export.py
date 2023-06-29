from typing import List, Union

from chat import Conversation, Message
from folder import FolderInterface
from prompt import Prompt

class ConversationV1:
    def __init__(self, id: int, name: str, messages: List[Message]):
        self.id = id
        self.name = name
        self.messages = messages

ExportFormatV1 = List[ConversationV1]

class ChatFolder:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

class ExportFormatV2:
    def __init__(self, history: Union[List[Conversation], None], folders: Union[List[ChatFolder], None]):
        self.history = history
        self.folders = folders

class ExportFormatV3:
    def __init__(self, history: List[Conversation], folders: List[FolderInterface]):
        self.version = 3
        self.history = history
        self.folders = folders

class ExportFormatV4:
    def __init__(self, history: List[Conversation], folders: List[FolderInterface], prompts: List[Prompt]):
        self.version = 4
        self.history = history
        self.folders = folders
        self.prompts = prompts

SupportedExportFormats = Union[ExportFormatV1, ExportFormatV2, ExportFormatV3, ExportFormatV4]
LatestExportFormat = ExportFormatV4
