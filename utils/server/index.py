import json
from typing import List
from io import BytesIO
import requests
from requests.exceptions import HTTPError
from streamlit.uploaded_file_manager import UploadedFile

from .constants import (
    AZURE_DEPLOYMENT_ID,
    OPENAI_API_HOST,
    OPENAI_API_TYPE,
    OPENAI_API_VERSION,
    OPENAI_ORGANIZATION,
)
from .models import OpenAIModel
from .types import Message
from .exceptions import OpenAIError


def OpenAIStream(
    model: OpenAIModel,
    systemPrompt: str,
    temperature: float,
    key: str,
    messages: List[Message],
    maxTokens: int,
):
    """
    Generates a stream of text completions using the OpenAI API.

    Args:
        model (OpenAIModel): The OpenAI model to use.
        systemPrompt (str): The system prompt.
        temperature (float): The temperature value for text generation.
        key (str): The API key to access the OpenAI API.
        messages (List[Message]): The list of messages.
        maxTokens (int): The maximum number of tokens for text completion.

    Returns:
        bytes: A stream of generated text completions.

    Raises:
        HTTPError: If there is an error with the HTTP request or response.
        OpenAIError: If the OpenAI API returns an error.
    """
    url = f"{OPENAI_API_HOST}/v1/chat/completions"
    if OPENAI_API_TYPE == "azure":
        url = f"{OPENAI_API_HOST}/openai/deployments/{AZURE_DEPLOYMENT_ID}/chat/completions?api-version={OPENAI_API_VERSION}"
    headers = {
        "Content-Type": "application/json",
    }
    if OPENAI_API_TYPE == "openai":
        headers["Authorization"] = f"Bearer {key or OPENAI_API_KEY}"
    elif OPENAI_API_TYPE == "azure":
        headers["api-key"] = f"{key or OPENAI_API_KEY}"
    if OPENAI_API_TYPE == "openai" and OPENAI_ORGANIZATION:
        headers["OpenAI-Organization"] = OPENAI_ORGANIZATION
    payload = {
        "messages": [
            {
                "role": "system",
                "content": systemPrompt,
            },
            *messages,
        ],
        "max_tokens": maxTokens,
        "temperature": temperature,
        "stream": True,
    }
    try:
        response = requests.post(url, headers=headers, json=payload, stream=True)
        response.raise_for_status()
        return response.iter_content(chunk_size=1024)
    except HTTPError as e:
        if response.headers.get("content-type") == "application/json":
            try:
                error = response.json().get("error")
                raise OpenAIError(
                    error["message"],
                    error["type"],
                    error["param"],
                    error["code"],
                )
            except (json.JSONDecodeError, KeyError):
                raise HTTPError(f"OpenAI API returned an error: {response.text}") from e
        else:
            raise HTTPError(f"OpenAI API returned an error: {response.text}") from e
