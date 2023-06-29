from typing import List, Union

from .chat import Message
from .openai import OpenAIModel
from .agent.plugins.executor import TaskExecutionContext

Action = {
    'type': 'action',
    'thought': str,
    'plugin': PluginSummary,
    'pluginInput': str
}
Answer = {
    'type': 'answer',
    'answer': str
}
ReactAgentResult = Union[Action, Answer]

class PlanningResponse:
    """
    Represents a planning response.

    Attributes:
        taskId (str): The task ID.
        result (ReactAgentResult): The result of the reaction agent.
    """

    def __init__(self, taskId: str, result: ReactAgentResult):
        self.taskId = taskId
        self.result = result

class PluginResult:
    """
    Represents a plugin result.

    Attributes:
        action (Action): The action.
        result (str): The result.
    """

    def __init__(self, action: Action, result: str):
        self.action = action
        self.result = result

class PlanningRequest:
    """
    Represents a planning request.

    Attributes:
        taskId (str, optional): The task ID.
        model (OpenAIModel): The OpenAI model.
        key (str, optional): The key.
        messages (List[Message]): The list of messages.
        enabledToolNames (List[str]): The list of enabled tool names.
        pluginResults (List[PluginResult]): The list of plugin results.
    """

    def __init__(self, taskId: str = None, model: OpenAIModel, key: str = None, messages: List[Message],
                 enabledToolNames: List[str], pluginResults: List[PluginResult]):
        self.taskId = taskId
        self.model = model
        self.key = key
        self.messages = messages
        self.enabledToolNames = enabledToolNames
        self.pluginResults = pluginResults

class RunPluginRequest:
    """
    Represents a run plugin request.

    Attributes:
        taskId (str): The task ID.
        model (OpenAIModel): The OpenAI model.
        input (str): The input.
        action (Action): The action.
        key (str, optional): The key.
    """

    def __init__(self, taskId: str, model: OpenAIModel, input: str, action: Action, key: str = None):
        self.taskId = taskId
        self.model = model
        self.input = input
        self.action = action
        self.key = key

class ToolDefinitionApi:
    """
    Represents a tool definition API.

    Attributes:
        type (str): The type.
        url (str): The URL.
        hasUserAuthentication (bool): Indicates whether user authentication is required.
    """

    def __init__(self, type: str, url: str, hasUserAuthentication: bool):
        self.type = type
        self.url = url
        self.hasUserAuthentication = hasUserAuthentication

class ToolAuth:
    """
    Represents tool authentication.

    Attributes:
        type (str): The type.
    """

    def __init__(self, type: str):
        self.type = type

class Plugin:
    """
    Represents a plugin.

    Attributes:
        nameForHuman (str): The name for human.
        nameForModel (str): The name for model.
        descriptionForModel (str): The description for model.
        descriptionForHuman (str): The description for human.
        execute (function): The execute function.
        api (ToolDefinitionApi, optional): The tool definition API.
        apiSpec (str, optional): The API specification.
        auth (ToolAuth, optional): The tool authentication.
        logoUrl (str, optional): The logo URL.
        contactEmail (str, optional): The contact email.
        legalInfoUrl (str, optional): The legal info URL.
        displayForUser (bool): Indicates whether the plugin should be displayed for the user.
    """

    def __init__(self, nameForHuman: str, nameForModel: str, descriptionForModel: str, descriptionForHuman: str,
                 execute: callable = None, api: ToolDefinitionApi = None, apiSpec: str = None, auth: ToolAuth = None,
                 logoUrl: str = None, contactEmail: str = None, legalInfoUrl: str = None, displayForUser: bool):
        self.nameForHuman = nameForHuman
        self.nameForModel = nameForModel
        self.descriptionForModel = descriptionForModel
        self.descriptionForHuman = descriptionForHuman
        self.execute = execute
        self.api = api
        self.apiSpec = apiSpec
        self.auth = auth
        self.logoUrl = logoUrl
        self.contactEmail = contactEmail
        self.legalInfoUrl = legalInfoUrl
        self.displayForUser = displayForUser

class RemotePluginTool(Plugin):
    """
    Represents a remote plugin tool.

    Inherits from Plugin and adds tool-specific attributes.

    Attributes:
        api (ToolDefinitionApi): The tool definition API.
        apiSpec (str): The API specification.
        auth (ToolAuth): The tool authentication.
    """

    def __init__(self, nameForHuman: str, nameForModel: str, descriptionForModel: str, descriptionForHuman: str,
                 api: ToolDefinitionApi, apiSpec: str, auth: ToolAuth, **kwargs):
        super().__init__(nameForHuman, nameForModel, descriptionForModel, descriptionForHuman, **kwargs)
        self.api = api
        self.apiSpec = apiSpec
        self.auth = auth

class PluginSummary:
    """
    Represents a plugin summary.

    Attributes:
        nameForHuman (str): The name for human.
        nameForModel (str): The name for model.
        descriptionForModel (str): The description for model.
        descriptionForHuman (str): The description for human.
        displayForUser (bool): Indicates whether the plugin should be displayed for the user.
        logoUrl (str, optional): The logo URL.
    """

    def __init__(self, nameForHuman: str, nameForModel: str, descriptionForModel: str, descriptionForHuman: str,
                 displayForUser: bool, logoUrl: str = None):
        self.nameForHuman = nameForHuman
        self.nameForModel = nameForModel
        self.descriptionForModel = descriptionForModel
        self.descriptionForHuman = descriptionForHuman
        self.displayForUser = displayForUser
        self.logoUrl = logoUrl
