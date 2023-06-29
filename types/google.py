from typing import List

class ChatBody:
    pass

class Message:
    pass

class GoogleBody(ChatBody):
    def __init__(self, googleAPIKey: str, googleCSEId: str):
        self.googleAPIKey = googleAPIKey
        self.googleCSEId = googleCSEId

class GoogleResponse:
    def __init__(self, message: Message):
        self.message = message

class GoogleSource:
    def __init__(self, title: str, link: str, displayLink: str, snippet: str, image: str, text: str):
        self.title = title
        self.link = link
        self.displayLink = displayLink
        self.snippet = snippet
        self.image = image
        self.text = text
