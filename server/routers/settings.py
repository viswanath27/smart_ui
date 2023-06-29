from utils.server.storage import UserDb
from types.settings import SettingsSchema
from trpc import procedure, router

async def get_settings(ctx):
    """
    Retrieve user settings from the database.

    Args:
        ctx (dict): The TRPC context.

    Returns:
        dict: The user settings.
    """
    try:
        userDb = await UserDb.fromUserHash(ctx['userHash'])
        return await userDb.getSettings()
    except Exception as e:
        print(e)
        raise e

async def update_settings(ctx, input):
    """
    Update user settings in the database.

    Args:
        ctx (dict): The TRPC context.
        input (dict): The updated settings.

    Returns:
        dict: The success status of the update.
    """
    userDb = await UserDb.fromUserHash(ctx['userHash'])
    await userDb.saveSettings(input)
    return {'success': True}

settings = router({
    'get': procedure.query(get_settings),
    'settingsUpdate': procedure.input(SettingsSchema).mutation(update_settings),
})
