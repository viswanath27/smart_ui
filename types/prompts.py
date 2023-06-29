from typing import List, Optional

import z3 as z

class OpenAIModelSchema:
    """
    Represents the schema for an OpenAI model.
    """

    # OpenAIModelSchema implementation goes here
    pass

PromptSchema = z3.schema(
    {
        "id": z3.string(),
        "name": z3.string(),
        "description": z3.string(),
        "content": z3.string(),
        "model": OpenAIModelSchema,
        "folderId": z3.string().optional(),
    }
)

PromptSchemaArray = z3.array(PromptSchema)

class Prompt:
    """
    Represents a prompt.
    """

    id: str
    name: str
    description: str
    content: str
    model: OpenAIModelSchema
    folderId: Optional[str]

    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        content: str,
        model: OpenAIModelSchema,
        folderId: Optional[str]
    ):
        self.id = id
        self.name = name
        self.description = description
        self.content = content
        self.model = model
        self.folderId = folderId

