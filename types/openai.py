from typing import Dict
import z3 as z

OPENAI_API_TYPE = "your_openai_api_type"

class OpenAIModelSchema:
    """
    Represents the schema for an OpenAI model.
    """

    id: str
    name: str
    maxLength: int
    tokenLimit: int

    def __init__(self, id: str, name: str, maxLength: int, tokenLimit: int):
        """
        Initializes the OpenAIModelSchema instance.

        Args:
            id (str): The ID of the model.
            name (str): The name of the model.
            maxLength (int): The maximum length of a message.
            tokenLimit (int): The token limit.
        """
        self.id = id
        self.name = name
        self.maxLength = maxLength
        self.tokenLimit = tokenLimit

OpenAIModel = OpenAIModelSchema

class OpenAIModelID:
    """
    Represents the available OpenAI model IDs.
    """

    GPT_3_5 = 'gpt-3.5-turbo'
    GPT_3_5_AZ = 'gpt-35-turbo'
    GPT_4 = 'gpt-4'
    GPT_4_32K = 'gpt-4-32k'

fallbackModelID = OpenAIModelID.GPT_3_5

OpenAIModels = {
    OpenAIModelID.GPT_3_5: OpenAIModelSchema(
        OpenAIModelID.GPT_3_5,
        'GPT-3.5',
        12000,
        4000
    ),
    OpenAIModelID.GPT_3_5_AZ: OpenAIModelSchema(
        OpenAIModelID.GPT_3_5_AZ,
        'GPT-3.5',
        12000,
        4000
    ),
    OpenAIModelID.GPT_4: OpenAIModelSchema(
        OpenAIModelID.GPT_4,
        'GPT-4',
        24000,
        8000
    ),
    OpenAIModelID.GPT_4_32K: OpenAIModelSchema(
        OpenAIModelID.GPT_4_32K,
        'GPT-4-32K',
        96000,
        32000
    ),
}
