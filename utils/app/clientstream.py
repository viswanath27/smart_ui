from typing import List
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

def update_conversation_from_stream(
    stream: AsyncGenerator[bytes, None],
    controller: Any,
    home_dispatch: Any,
    updated_conversation: Conversation,
    stop_conversation_ref: Any
) -> Conversation:
    """
    Updates the conversation from a stream of bytes.

    Args:
        stream (AsyncGenerator[bytes, None]): The stream of bytes to read.
        controller (Any): The controller for the conversation stream.
        home_dispatch (Any): The dispatcher for updating the home screen.
        updated_conversation (Conversation): The initial conversation state.
        stop_conversation_ref (Any): The reference for stopping the conversation.

    Returns:
        Conversation: The updated conversation after reading the stream.

    Raises:
        StopAsyncIteration: If the stream reading is stopped.
    """
    reader = stream.__aiter__()
    decoder = TextDecoder()
    done = False
    is_first = True
    text = ''
    while not done:
        if stop_conversation_ref.current:
            stop_conversation_ref.current = False
            controller.abort()
            done = True
            break
        try:
            value = await reader.__anext__()
            done_reading = False
        except StopAsyncIteration:
            done = True
            done_reading = True
        chunk_value = decoder.decode(value)
        text += chunk_value
        if is_first:
            is_first = False
            updated_messages = [
                *updated_conversation['messages'],
                {'role': 'assistant', 'content': chunk_value},
            ]
            updated_conversation = {
                **updated_conversation,
                'messages': updated_messages,
            }
            home_dispatch({
                'field': 'selectedConversation',
                'value': updated_conversation,
            })
        else:
            updated_messages = [
                {
                    **message,
                    'content': text,
                } if index == len(updated_conversation['messages']) - 1 else message
                for index, message in enumerate(updated_conversation['messages'])
            ]
            updated_conversation = {
                **updated_conversation,
                'messages': updated_messages,
            }
            home_dispatch({
                'field': 'selectedConversation',
                'value': updated_conversation,
            })
    return updated_conversation
