from trpc import router
from .conversations import conversations
from .folders import folders
from .models import models
from .prompts import prompts
from .settings import settings

def appRouter():
    """
    Application router that handles different routes and operations.
    
    Returns:
        The application router.
    """
    return router(
        models=models,
        settings=settings,
        prompts=prompts,
        folders=folders,
        conversations=conversations
    )

# Type definition of API
AppRouter = type(appRouter)
