from utils.server.storage import UserDb
from types.folder import FolderSchema, FolderSchemaArray
from trpc import procedure, router
from z3 import z

def folders():
    """
    Router for handling folder operations.
    """
    return router(
        list=procedure.query(async ({ ctx }) => {
            """
            Retrieves a list of folders for the user.
            
            Args:
                ctx: The context object.
            
            Returns:
                A list of folders.
            """
            userDb = await UserDb.fromUserHash(ctx.userHash)
            return await userDb.getFolders()
        }),
        remove=procedure.input(z.object({ id: z.string() })).mutation(async ({ ctx, input }) => {
            """
            Removes a folder.

            Args:
                ctx: The context object.
                input: The input object containing the folder ID.

            Returns:
                A dictionary indicating the success of the operation.
            """
            userDb = await UserDb.fromUserHash(ctx.userHash)
            await userDb.removeFolder(input.id)
            return { success: True }
        }),
        removeAll=procedure.input(z.object({ type: z.string() })).mutation(async ({ ctx, input }) => {
            """
            Removes all folders of a given type.

            Args:
                ctx: The context object.
                input: The input object containing the folder type.

            Returns:
                A dictionary indicating the success of the operation.
            """
            userDb = await UserDb.fromUserHash(ctx.userHash)
            await userDb.removeAllFolders(input.type)
            return { success: True }
        }),
        update=procedure.input(FolderSchema).mutation(async ({ ctx, input }) => {
            """
            Updates a folder.

            Args:
                ctx: The context object.
                input: The input object containing the folder data.

            Returns:
                A dictionary indicating the success of the operation.
            """
            userDb = await UserDb.fromUserHash(ctx.userHash)
            await userDb.saveFolder(input)
            return { success: True }
        }),
        updateAll=procedure.input(FolderSchemaArray).mutation(async ({ ctx, input }) => {
            """
            Updates multiple folders.

            Args:
                ctx: The context object.
                input: The input object containing an array of folder data.

            Returns:
                A dictionary indicating the success of the operation.
            """
            userDb = await UserDb.fromUserHash(ctx.userHash)
            await userDb.saveFolders(input)
            return { success: True }
        }),
    )
