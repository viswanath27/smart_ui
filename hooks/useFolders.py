from typing import List, Tuple, Callable
import React
from utils.trpc import trpc
from types.chat import Conversation
from types.folder import FolderInterface, FolderType
from types.prompt import Prompt
from pages.api.home.home_context import HomeContext
from uuid import uuid4

FoldersAction = {
    "update": Callable[[FolderInterface], Promise[List[FolderInterface]]],
    "updateAll": Callable[[List[FolderInterface]], Promise[List[FolderInterface]]],
    "add": Callable[[str, FolderType], Promise[List[FolderInterface]]],
    "remove": Callable[[str], Promise[List[FolderInterface]]],
    "clear": Callable[[], Promise[List[FolderInterface]]]
}

def useFolders() -> Tuple[List[FolderInterface], FoldersAction]:
    """
    Custom hook for managing folders.

    Returns:
        A tuple containing the list of folders and the folder actions.
    """
    promptsUpdateAll = trpc.prompts.updateAll.useMutation()
    conversationUpdateAll = trpc.conversations.updateAll.useMutation()
    folderUpdateAll = trpc.folders.updateAll.useMutation()
    folderUpdate = trpc.folders.update.useMutation()
    folderRemove = trpc.folders.remove.useMutation()
    folderRemoveAll = trpc.folders.removeAll.useMutation()
    homeContext = useContext(HomeContext)
    folders = homeContext['state']['folders']
    conversations = homeContext['state']['conversations']
    prompts = homeContext['state']['prompts']
    dispatch = homeContext['dispatch']

    def updateAll(updated: List[FolderInterface]) -> Promise[List[FolderInterface]]:
        """
        Updates all folders.

        Args:
            updated: The updated list of folders.

        Returns:
            The updated list of folders.
        """
        folderUpdateAll.mutateAsync(updated)
        dispatch({ 'field': 'folders', 'value': updated })
        return updated

    def add(name: str, type: FolderType) -> Promise[List[FolderInterface]]:
        """
        Adds a new folder.

        Args:
            name: The name of the new folder.
            type: The type of the new folder.

        Returns:
            The updated list of folders.
        """
        newFolder: FolderInterface = {
            'id': uuid4(),
            'name': name,
            'type': type
        }
        newState = [newFolder] + folders
        folderUpdate.mutateAsync(newFolder)
        dispatch({ 'field': 'folders', 'value': newState })
        return newState

    def update(folder: FolderInterface) -> Promise[List[FolderInterface]]:
        """
        Updates a specific folder.

        Args:
            folder: The updated folder.

        Returns:
            The updated list of folders.
        """
        newState = [folder if f['id'] == folder['id'] else f for f in folders]
        folderUpdate.mutateAsync(folder)
        dispatch({ 'field': 'folders', 'value': newState })
        return newState

    def clear() -> Promise[List[FolderInterface]]:
        """
        Clears the folders.

        Returns:
            The updated list of folders.
        """
        newState = [f for f in folders if f['type'] != 'chat']
        folderRemoveAll.mutateAsync({ 'type': 'chat' })
        dispatch({ 'field': 'folders', 'value': newState })
        return newState

    def remove(folderId: str) -> Promise[List[FolderInterface]]:
        """
        Removes a specific folder.

        Args:
            folderId: The ID of the folder to be removed.

        Returns:
            The updated list of folders.
        """
        newState = [f for f in folders if f['id'] != folderId```
        folderRemove.mutateAsync({ 'id': folderId })
        dispatch({ 'field': 'folders', 'value': newState })

        targetConversations: List[Conversation] = []
        updatedConversations: List[Conversation] = [c if c['folderId'] != folderId else { **c, 'folderId': None } for c in conversations]
        for c in conversations:
            if c['folderId'] == folderId:
                targetConversations.append(c)
                updatedConversations.append({ **c, 'folderId': None })

        conversationUpdateAll.mutateAsync(targetConversations)
        dispatch({ 'field': 'conversations', 'value': updatedConversations })

        updatedPrompts: List[Prompt] = [{ **p, 'folderId': None } if p['folderId'] == folderId else p for p in prompts]

        promptsUpdateAll.mutateAsync(updatedPrompts)
        dispatch({ 'field': 'prompts', 'value': updatedPrompts })

        return newState

    return folders, {
        'add': add,
        'update': update,
        'updateAll': updateAll,
        'remove': remove,
        'clear': clear
    }
