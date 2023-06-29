from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from typing import List
import os

MONGODB_DB = "your_mongodb_db_name"

class Conversation:
    """
    Represents a conversation.
    """

class FolderInterface:
    """
    Represents a folder interface.
    """

class Prompt:
    """
    Represents a prompt.
    """

class Settings:
    """
    Represents user settings.
    """

def get_db() -> Database:
    """
    Retrieves the MongoDB database instance.

    Returns:
        Database: The MongoDB database instance.

    Raises:
        ValueError: If the MONGODB_URI environment variable is not set.
    """
    if not "MONGODB_URI" in os.environ:
        raise ValueError("MONGODB_URI is not set")

    client = MongoClient(os.environ["MONGODB_URI"])
    db = client[MONGODB_DB]
    return db

class UserDb:
    def __init__(self, db: Database, user_id: str):
        self._conversations: Collection = db["conversations"]
        self._folders: Collection = db["folders"]
        self._prompts: Collection = db["prompts"]
        self._settings: Collection = db["settings"]
        self._user_id = user_id

    @staticmethod
    async def from_user_hash(user_id: str) -> "UserDb":
        """
        Creates a UserDb instance from the user ID.

        Args:
            user_id (str): The user ID.

        Returns:
            UserDb: The UserDb instance.
        """
        db = await get_db()
        return UserDb(db, user_id)

    async def get_conversations(self) -> List[Conversation]:
        """
        Retrieves all conversations for the user.

        Returns:
            List[Conversation]: A list of Conversation objects representing the user's conversations.
        """
        return await self._conversations.find({"userId": self._user_id}).sort("_id", -1).toArray()

    async def save_conversation(self, conversation: Conversation):
        """
        Saves a conversation for the user.

        Args:
            conversation (Conversation): The Conversation object to be saved.
        """
        await self._conversations.update_one(
            {"userId": self._user_id, "conversation.id": conversation.id},
            {"$set": {"conversation": conversation}},
            upsert=True,
        )

    async def save_conversations(self, conversations: List[Conversation]):
        """
        Saves multiple conversations for the user.

        Args:
            conversations (List[Conversation]): A list of Conversation objects to be saved.
        """
        for conversation in conversations:
            await self.save_conversation(conversation)

    def remove_conversation(self, id: str):
        """
        Removes a conversation for the user by ID.

        Args:
            id (str): The ID of the conversation to be removed.
        """
        self._conversations.delete_one({"userId": self._user_id, "conversation.id": id})

    def remove_all_conversations(self):
        """
        Removes all conversations for the user.
        """
        self._conversations.delete_many({"userId": self._user_id})

    async def get_folders(self) -> List[FolderInterface]:
        """
        Retrieves all folders for the user.

        Returns:
            List[FolderInterface]: A list of FolderInterface objects representing the user's folders.
        """
        items = await self._folders.find({"userId": self._user_id}).sort("folder.name", 1).toArray()
        return [item["folder"] for item in items]

    async def save_folder(self, folder: FolderInterface):
        """
        Saves a folder for the user.

        Args:
            folder (FolderInterface): The FolderInterface object to be saved.
        """
        await self._folders.update_one(
            {"userId": self._user_id, "folder.id": folder.id},
            {"$set": {"folder": folder}},
            upsert=True,
        )

    async def save_folders(self, folders: List[FolderInterface]):
        """
        Saves multiple folders for the user.

        Args:
            folders (List[FolderInterface]): A list of FolderInterface objects to be saved.
        """
        for folder in folders:
            await self.save_folder(folder)

    async def remove_folder(self, id: str):
        """
        Removes a folder for the user by ID.

        Args:
            id (str): The ID of the folder to be removed.
        """
        await self._folders.delete_one({"userId": self._user_id, "folder.id": id})

    async def remove_all_folders(self, type: str):
        """
        Removes all folders for the user of a specific type.

        Args:
            type (str): The type of folders to be removed.
        """
        await self._folders.delete_many({"userId": self._user_id, "folder.type": type})

    async def get_prompts(self) -> List[Prompt]:
        """
        Retrieves all prompts for the user.

        Returns:
            List[Prompt]: A list of Prompt objects representing the user's prompts.
        """
        items = await self._prompts.find({"userId": self._user_id}).sort("prompt.name", 1).toArray()
        return [item["prompt"] for item in items]

    async def save_prompt(self, prompt: Prompt):
        """
        Saves a prompt for the user.

        Args:
            prompt (Prompt): The Prompt object to be saved.
        """
        await self._prompts.update_one(
            {"userId": self._user_id, "prompt.id": prompt.id},
            {"$set": {"prompt": prompt}},
            upsert=True,
        )

    async def save_prompts(self, prompts: List[Prompt]):
        """
        Saves multiple prompts for the user.

        Args:
            prompts (List[Prompt]): A list of Prompt objects to be saved.
        """
        for prompt in prompts:
            await self.save_prompt(prompt)

    async def remove_prompt(self, id: str):
        """
        Removes a prompt for the user by ID.

        Args:
            id (str): The ID of the prompt to be removed.
        """
        await self._prompts.delete_one({"userId": self._user_id, "prompt.id": id})

    async def get_settings(self) -> Settings:
        """
        Retrieves the user's settings.

        Returns:
            Settings: The user's settings.
        """
        item = await self._settings.find_one({"userId": self._user_id})
        if item:
            return item["settings"]
        return Settings(userId=self._user_id, theme="dark", defaultTemperature=1.0)

    async def save_settings(self, settings: Settings):
        """
        Saves the user's settings.

        Args:
            settings (Settings): The user's settings to be saved.
        """
        settings.userId = self._user_id
        await self._settings.update_one(
            {"userId": self._user_id},
            {"$set": {"settings": settings}},
            upsert=True,
        )
