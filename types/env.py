class ProcessEnv:
    """
    Represents the environment variables used in the application.

    Attributes:
        OPENAI_API_KEY (str): The API key for OpenAI.
        OPENAI_API_HOST (str, optional): The host for the OpenAI API.
        OPENAI_API_TYPE (str, optional): The type of the OpenAI API (either 'openai' or 'azure').
        OPENAI_API_VERSION (str, optional): The version of the OpenAI API.
        OPENAI_ORGANIZATION (str, optional): The organization associated with the OpenAI API.
        NEXT_PUBLIC_DEFAULT_SYSTEM_PROMPT (str): The default system prompt for the application.
        MONGODB_URI (str): The URI for the MongoDB database.
        MONGODB_DB (str): The name of the MongoDB database.
        GITHUB_CLIENT_ID (str, optional): The client ID for GitHub authentication.
        GITHUB_CLIENT_SECRET (str, optional): The client secret for GitHub authentication.
        GOOGLE_CLIENT_ID (str, optional): The client ID for Google authentication.
        GOOGLE_CLIENT_SECRET (str, optional): The client secret for Google authentication.
        NEXTAUTH_ENABLED ('true' or 'false'): Indicates whether NextAuth is enabled.
        NEXTAUTH_EMAIL_PATTERN (str, optional): The email pattern for NextAuth.
    """

    def __init__(
        self,
        OPENAI_API_KEY: str,
        OPENAI_API_HOST: str = None,
        OPENAI_API_TYPE: str = None,
        OPENAI_API_VERSION: str = None,
        OPENAI_ORGANIZATION: str = None,
        NEXT_PUBLIC_DEFAULT_SYSTEM_PROMPT: str,
        MONGODB_URI: str,
        MONGODB_DB: str,
        GITHUB_CLIENT_ID: str = None,
        GITHUB_CLIENT_SECRET: str = None,
        GOOGLE_CLIENT_ID: str = None,
        GOOGLE_CLIENT_SECRET: str = None,
        NEXTAUTH_ENABLED: str,
        NEXTAUTH_EMAIL_PATTERN: str = None,
    ):
        self.OPENAI_API_KEY = OPENAI_API_KEY
        self.OPENAI_API_HOST = OPENAI_API_HOST
        self.OPENAI_API_TYPE = OPENAI_API_TYPE
        self.OPENAI_API_VERSION = OPENAI_API_VERSION
        self.OPENAI_ORGANIZATION = OPENAI_ORGANIZATION
        self.NEXT_PUBLIC_DEFAULT_SYSTEM_PROMPT = NEXT_PUBLIC_DEFAULT_SYSTEM_PROMPT
        self.MONGODB_URI = MONGODB_URI
        self.MONGODB_DB = MONGODB_DB
        self.GITHUB_CLIENT_ID = GITHUB_CLIENT_ID
        self.GITHUB_CLIENT_SECRET = GITHUB_CLIENT_SECRET
        self.GOOGLE_CLIENT_ID = GOOGLE_CLIENT_ID
        self.GOOGLE_CLIENT_SECRET = GOOGLE_CLIENT_SECRET
        self.NEXTAUTH_ENABLED = NEXTAUTH_ENABLED
        self.NEXTAUTH_EMAIL_PATTERN = NEXTAUTH_EMAIL_PATTERN
