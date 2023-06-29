import z3 as z

class SettingsSchema:
    """
    Represents the schema for the settings.
    """

    userId: str
    theme: str
    defaultTemperature: float

    def __init__(self, userId: str, theme: str, defaultTemperature: float):
        """
        Initializes the SettingsSchema instance.

        Args:
            userId (str): The user ID.
            theme (str): The theme (either 'light' or 'dark').
            defaultTemperature (float): The default temperature.
        """
        self.userId = userId
        self.theme = theme
        self.defaultTemperature = defaultTemperature

Settings = SettingsSchema
