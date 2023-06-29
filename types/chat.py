from typing import List, Optional, Union

from .agent import Plugin
from .openai import OpenAIModelSchema

import z3

RoleSchema = z3.z3.Union([z3.z3.Literal('system'), z3.z3.Literal('assistant'), z3.z3.Literal('user')])
Role = z3.z3.InferType[RoleSchema]

MessageSchema = z3.z3.Object({
  'role': RoleSchema,
  'content': z3.z3.String(),
})
Message = z3.z3.InferType[MessageSchema]

ChatBodySchema = z3.z3.Object({
  'model': OpenAIModelSchema,
  'messages': z3.z3.Array(MessageSchema),
  'key': z3.z3.String(),
  'prompt': z3.z3.String(),
  'temperature': z3.z3.Number(),
  'googleAPIKey': z3.z3.String().optional(),
  'googleCSEId': z3.z3.String().optional(),
})
ChatBody = z3.z3.InferType[ChatBodySchema]

class ChatModeRunner:
    """
    Represents a chat mode runner.
    """

    def run(self, params: ChatModeRunnerParams) -> None:
        """
        Runs the chat mode.

        Args:
            params (ChatModeRunnerParams): The parameters for running the chat mode.
        """
        pass

class ChatModeRunnerParams:
    """
    Represents the parameters for a chat mode runner.

    Attributes:
        body (ChatBody): The chat body.
        message (Message): The message.
        conversation (Conversation): The conversation.
        selectedConversation (Conversation): The selected conversation.
        plugins (List[Plugin]): The plugins.
    """

    def __init__(self, body: ChatBody, message: Message, conversation: Conversation,
                 selectedConversation: Conversation, plugins: List[Plugin]):
        self.body = body
        self.message = message
        self.conversation = conversation
        self.selectedConversation = selectedConversation
        self.plugins = plugins

ConversationSchema = z3.z3.Object({
  'id': z3.z3.String(),
  'name': z3.z3.String(),
  'messages': z3.z3.Array(MessageSchema),
  'model': OpenAIModelSchema,
  'prompt': z3.z3.String(),
  'temperature': z3.z3.Number(),
  'folderId': z3.z3.String().optional(),
})
Conversation = z3.z3.InferType[ConversationSchema]
ConversationSchemaArray = z3.z3.Array(ConversationSchema)
