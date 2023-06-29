from typing import Any, List, Union
from datetime import date

from fastapi import FastAPI
from pydantic import BaseModel

class Conversation(BaseModel):
    # Define the Conversation data model
    pass

class ExportFormatV1(BaseModel):
    # Define the ExportFormatV1 data model
    pass

class ExportFormatV2(BaseModel):
    # Define the ExportFormatV2 data model
    pass

class ExportFormatV3(BaseModel):
    # Define the ExportFormatV3 data model
    pass

class ExportFormatV4(BaseModel):
    # Define the ExportFormatV4 data model
    pass

class LatestExportFormat(BaseModel):
    # Define the LatestExportFormat data model
    pass

class FolderInterface(BaseModel):
    # Define the FolderInterface data model
    pass

class Prompt(BaseModel):
    # Define the Prompt data model
    pass

class Settings(BaseModel):
    # Define the Settings data model
    pass

def isExportFormatV1(obj: Any) -> bool:
    """
    Check if the given object matches ExportFormatV1.

    Args:
        obj (Any): The object to check.

    Returns:
        bool: True if the object matches ExportFormatV1, False otherwise.
    """
    return isinstance(obj, list)

def isExportFormatV2(obj: Any) -> bool:
    """
    Check if the given object matches ExportFormatV2.

    Args:
        obj (Any): The object to check.

    Returns:
        bool: True if the object matches ExportFormatV2, False otherwise.
    """
    return not hasattr(obj, 'version') and hasattr(obj, 'folders') and hasattr(obj, 'history')

def isExportFormatV3(obj: Any) -> bool:
    """
    Check if the given object matches ExportFormatV3.

    Args:
        obj (Any): The object to check.

    Returns:
        bool: True if the object matches ExportFormatV3, False otherwise.
    """
    return obj.version == 3

def isExportFormatV4(obj: Any) -> bool:
    """
    Check if the given object matches ExportFormatV4.

    Args:
        obj (Any): The object to check.

    Returns:
        bool: True if the object matches ExportFormatV4, False otherwise.
    """
    return obj.version == 4

isLatestExportFormat = isExportFormatV4

class CleaningFallback(BaseModel):
    temperature: float

def cleanData(data: Union[ExportFormatV1, ExportFormatV2, ExportFormatV3, ExportFormatV4],
              fallback: CleaningFallback) -> LatestExportFormat:
    """
    Clean the given data based on its export format.

    Args:
        data (Union[ExportFormatV1, ExportFormatV2, ExportFormatV3, ExportFormatV4]): The export data to clean.
        fallback (CleaningFallback): The fallback values.

    Returns:
        LatestExportFormat: The cleaned export data.

    Raises:
        ValueError: If the data format is unsupported.
    """
    if isExportFormatV1(data):
        return LatestExportFormat(
            version=4,
            history=cleanConversationHistory(data, fallback),
            folders=[],
            prompts=[]
        )
    if isExportFormatV2(data):
        folders = [FolderInterface(id=str(chatFolder.id), name=chatFolder.name, type='chat')
                   for chatFolder in (data.folders or [])]
        return LatestExportFormat(
            version=4,
            history=cleanConversationHistory(data.history or [], fallback),
            folders=folders,
            prompts=[]
        )
    if isExportFormatV3(data):
        return LatestExportFormat(**data.dict(), version=4, prompts=[])
    if isExportFormatV4(data):
        return data
    raise ValueError('Unsupported data format')

def currentDate() -> str:
    """
    Get the current date in the format 'month-day'.

    Returns:
        str: The current date.
    """
    today = date.today()
    return today.strftime("%m-%d")

def exportData(history: List[Conversation], folders: List[FolderInterface], prompts: List[Prompt]) -> None:
    """
    Export the given data to a JSON file.

    Args:
        history (List[Conversation]): The conversation history.
        folders (List[FolderInterface]): The folders.
        prompts (List[Prompt]): The prompts.
    """
    data = LatestExportFormat(
        version=4,
        history=history or [],
        folders=folders or [],
        prompts=prompts or []
    )
    # Export the data to a JSON file
    json_data = data.json(indent=2)
    file_name = f"chatbot_ui_history_{currentDate()}.json"
    with open(file_name, 'w') as file:
        file.write(json_data)

