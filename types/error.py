class ErrorMessage:
    """
    Represents an error message.

    Attributes:
        code (str or None): The error code.
        title (str): The title of the error.
        messageLines (list of str): The lines of the error message.
    """

    def __init__(self, code: str or None, title: str, messageLines: list of str):
        self.code = code
        self.title = title
        self.messageLines = messageLines
