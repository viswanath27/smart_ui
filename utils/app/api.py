from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatMode(BaseModel):
    # Define the ChatMode fields
    # Replace with the actual fields and types

class ChatModeID(BaseModel):
    # Define the ChatModeID fields
    # Replace with the actual fields and types

def get_endpoint(plugin: Optional[ChatMode]) -> str:
    if not plugin:
        return 'api/chat'

    if plugin.id == ChatModeID.GOOGLE_SEARCH:
        return 'api/google'

    return 'api/chat'

async def watch_ref_to_abort(ref: bool, fn: callable) -> R:
    controller = AbortController()
    interval = None
    try:
        interval = setInterval(
            lambda: (
                if ref:
                    ref = False
                    controller.abort()
                    if interval:
                        clearInterval(interval)
                        interval = None
            ),
            200
        )
        return await fn(controller)
    finally:
        if interval:
            clearInterval(interval)

