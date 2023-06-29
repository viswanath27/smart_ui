from typing import List, Optional
from pydantic import BaseModel

class Conversation(BaseModel):
    # Define the Conversation fields
    # Replace with the actual fields and types

class OpenAIModelID(BaseModel):
    # Define the OpenAIModelID fields
    # Replace with the actual fields and types

class OpenAIModels(BaseModel):
    # Define the OpenAIModels fields
    # Replace with the actual fields and types

class Settings(BaseModel):
    # Define the Settings fields
    # Replace with the actual fields and types

DEFAULT_SYSTEM_PROMPT = 'default_system_prompt'

def clean_selected_conversation(settings: Settings, conversation: Conversation) -> Conversation:
    updated_conversation = conversation

    # Check for model on each conversation
    if not updated_conversation.model:
        updated_conversation.model = OpenAIModels[OpenAIModelID.GPT_3_5]

    # Check for system prompt on each conversation
    if not updated_conversation.prompt:
        updated_conversation.prompt = DEFAULT_SYSTEM_PROMPT

    if not updated_conversation.temperature:
        updated_conversation.temperature = settings.defaultTemperature

    if not updated_conversation.folderId:
        updated_conversation.folderId = None

    return updated_conversation

def clean_conversation_history(history: List[Conversation], fallback: dict) -> List[Conversation]:
    if not isinstance(history, list):
        print('history is not an array. Returning an empty array.')
        return []

    cleaned_history = []
    for conversation in history:
        try:
            if not conversation.model:
                conversation.model = OpenAIModels[OpenAIModelID.GPT_3_5]

            if not conversation.prompt:
                conversation.prompt = DEFAULT_SYSTEM_PROMPT

            if not conversation.temperature:
                conversation.temperature = fallback['temperature']

            if not conversation.folderId:
                conversation.folderId = None

            cleaned_history.append(conversation)
        except Exception as error:
            print('Error while cleaning conversations\' history. Removing culprit:', error)

    return cleaned_history

