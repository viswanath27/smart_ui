from typing import Dict, Any, List
from tiktoken import Tiktoken


def create_messages_to_send(
    encoding: Tiktoken,
    model: Dict[str, Any],
    system_prompt: str,
    reserved_for_completion: int,
    messages: List[Dict[str, str]]
) -> Dict[str, Any]:
    """
    Creates the messages to send for text completion based on the given parameters.

    Args:
        encoding (Tiktoken): The Tiktoken encoding instance.
        model (Dict[str, Any]): The model information.
        system_prompt (str): The system prompt.
        reserved_for_completion (int): The number of tokens reserved for completion.
        messages (List[Dict[str, str]]): The list of messages.

    Returns:
        Dict[str, Any]: The messages to send for text completion.

    """
    messages_to_send: List[Dict[str, str]] = []
    system_prompt_message = {
        "role": "system",
        "content": system_prompt
    }

    content_length = 0
    for i in range(len(messages) - 1, -1, -1):
        message = messages[i]
        serializing_messages = [
            system_prompt_message,
            *messages_to_send,
            message
        ]
        serialized = serialize_messages(model["name"], serializing_messages)
        encoded_length = len(encoding.encode(serialized, "all"))
        if encoded_length + reserved_for_completion > model["tokenLimit"]:
            break
        content_length = encoded_length
        messages_to_send = [message, *messages_to_send]

    max_token = model["tokenLimit"] - content_length
    return {
        "messages": messages_to_send,
        "maxToken": max_token
    }


def serialize_messages(model: str, messages: List[Dict[str, str]]) -> str:
    """
    Serializes the messages into a string representation.

    Args:
        model (str): The model name.
        messages (List[Dict[str, str]]): The list of messages.

    Returns:
        str: The serialized messages.

    """
    is_chat = "gpt-3.5-turbo" in model or "gpt-4" in model
    msg_sep = "\n" if is_chat else ""
    role_sep = "\n" if is_chat else ""
    return f"{msg_sep.join([f'{message['role']}{role_sep}{message['content']}' for message in messages])}{msg_sep}assistant{role_sep}"
