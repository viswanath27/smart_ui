from typing import Any, Dict
from utils.app.importExport import exportData
from utils.trpc import trpc
from pages.api.home.home_context import HomeContext

def useExporter():
    """
    Custom hook for exporting data.

    Returns:
        A dictionary with an `exportData` function for exporting data.
    """
    conversationsListQuery = trpc.conversations.list.useQuery(None, {
        'enabled': False
    })
    foldersListQuery = trpc.folders.list.useQuery(None, {
        'enabled': False
    })
    promptsListQuery = trpc.prompts.list.useQuery(None, {
        'enabled': False
    })
    homeContext = useContext(HomeContext)
    prompts = homeContext['state']['prompts']

    def exportData():
        """
        Exports data.

        Raises:
            Error: If there is an error in fetching the data.

        Returns:
            None.
        """
        conversationsResult = conversationsListQuery.refetch()
        if conversationsResult.isError:
            raise conversationsResult.error

        foldersResult = foldersListQuery.refetch()
        if foldersResult.isError:
            raise foldersResult.error

        promptsResult = promptsListQuery.refetch()
        if promptsResult.isError:
            raise promptsResult.error

        exportData(
            conversationsResult.data,
            foldersResult.data,
            promptsResult.data
        )

    return {
        'exportData': exportData
    }
