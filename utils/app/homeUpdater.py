from typing import List
from fastapi import FastAPI

class HomeUpdater:
    def __init__(self, app: FastAPI):
        """
        Initialize the HomeUpdater with the given FastAPI instance.

        Args:
            app (FastAPI): The FastAPI instance.
        """
        self.app = app

    def add_message(self, conversation: dict, message: dict) -> dict:
        """
        Add a message to the conversation.

        Args:
            conversation (dict): The conversation dictionary.
            message (dict): The message to be added.

        Returns:
            dict: The updated conversation dictionary.
        """
        updated_messages = conversation["messages"] + [message]
        conversation["messages"] = updated_messages
        self.app.dispatch({
            "field": "selectedConversation",
            "value": conversation
        })
        return conversation

    def append_chunk_to_last_message(self, conversation: dict, chunk: str) -> dict:
        """
        Append a chunk to the last message in the conversation.

        Args:
            conversation (dict): The conversation dictionary.
            chunk (str): The chunk to be appended.

        Returns:
            dict: The updated conversation dictionary.
        """
        last_index = len(conversation["messages"]) - 1
        last_message = conversation["messages"][last_index]
        messages = conversation["messages"][:last_index] + [last_message]
        conversation["messages"] = messages
        self.app.dispatch({
            "field": "selectedConversation",
            "value": conversation
        })
        return conversation

