from typing import Any, Dict
from utils.app.importExport import cleanData
from utils.trpc import trpc
from types.export import SupportedExportFormats
from types.settings import Settings

def useImporter() -> Dict[str, Any]:
    """
    Custom hook for importing data.

    Returns:
        A dictionary with an `importData` function for importing data.
    """
    conversationsMutation = trpc.conversations.updateAll.useMutation()
    foldersMutation = trpc.folders.updateAll.useMutation()
    promptsMutation = trpc.prompts.updateAll.useMutation()

    def importData(settings: Settings, data: SupportedExportFormats):
        """
        Imports data.

        Args:
            settings: The settings object.
            data: The data to be imported.

        Returns:
            The cleaned data.
        """
        cleanedData = cleanData(data, {
            'temperature': settings.defaultTemperature
        })
        history = cleanedData['history']
        folders = cleanedData['folders']
        prompts = cleanedData['prompts']
        conversations = history
        conversationsMutation.mutateAsync(conversations)
        foldersMutation.mutateAsync(folders)
        promptsMutation.mutateAsync(prompts)
        return cleanedData

    return {
        'importData': importData
    }
