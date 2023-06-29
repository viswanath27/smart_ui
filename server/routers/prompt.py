from utils.server.storage import UserDb
from types.prompt import PromptSchema, PromptSchemaArray
from trpc import procedure, router
from zod import z

async def get_prompts(ctx):
    """
    Retrieve prompts from the database.

    Args:
        ctx (dict): The TRPC context.

    Returns:
        list: The prompts.
    """
    userDb = await UserDb.fromUserHash(ctx['userHash'])
    return await userDb.getPrompts()

async def remove_prompt(ctx, input):
    """
    Remove a prompt from the database.

    Args:
        ctx (dict): The TRPC context.
        input (dict): The prompt ID to remove.

    Returns:
        dict: The success status of the removal.
    """
    userDb = await UserDb.fromUserHash(ctx['userHash'])
    await userDb.removePrompt(input['id'])
    return {'success': True}

async def update_prompt(ctx, input):
    """
    Update a prompt in the database.

    Args:
        ctx (dict): The TRPC context.
        input (dict): The updated prompt.

    Returns:
        dict: The success status of the update.
    """
    userDb = await UserDb.fromUserHash(ctx['userHash'])
    await userDb.savePrompt(input)
    return {'success': True}

async def update_all_prompts(ctx, input):
    """
    Update multiple prompts in the database.

    Args:
        ctx (dict): The TRPC context.
        input (list): The updated prompts.

    Returns:
        dict: The success status of the update.
    """
    userDb = await UserDb.fromUserHash(ctx['userHash'])
    await userDb.savePrompts(input)
    return {'success': True}

prompts = router({
    'list': procedure.query(get_prompts),
    'remove': procedure.input(z.object({'id': z.string()})).mutation(remove_prompt),
    'update': procedure.input(PromptSchema).mutation(update_prompt),
    'updateAll': procedure.input(PromptSchemaArray).mutation(update_all_prompts),
})
