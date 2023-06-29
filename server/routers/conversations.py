from utils.server.storage import UserDb
from types.chat import ConversationSchema, ConversationSchemaArray
from trpc import procedure, router
from z3 import z

def conversations():
    """
    Router for handling conversation operations.
    """
    return router(
        list=procedure.query(async ({ ctx }) => {
            """
            Retrieves a list of conversations for the user.
            
            Args:
                ctx: The context object.
            
            Returns:
                A list of conversations.
            """
            userDb = await UserDb.fromUserHash(ctx.userHash)
            return await userDb.getConversations()
        }),
        remove=procedure.input(z.object({ id: z.string() })).mutation(async ({ ctx, input }) => {
            """
            Removes a conversation.

            Args:
                ctx: The context object.
                input: The input object containing the conversation ID.

            Returns:
                A dictionary indicating the success of the operation.
            """
            userDb = await UserDb.fromUserHash(ctx.userHash)
            await userDb.removeConversation(input.id)
            return { success: True }
        }),
        removeAll=procedure.mutation(async ({ ctx }) => {
            """
            Removes all conversations.

            Args:
                ctx: The context object.

            Returns:
                A dictionary indicating the success of the operation.
            """
            userDb = await UserDb.fromUserHash(ctx.userHash)
            await userDb.removeAllConversations()
            return { success: True }
        }),
        update=procedure.input(ConversationSchema).mutation(async ({ ctx, input }) => {
            """
            Updates a conversation.

            Args:
                ctx: The context object.
                input: The input object containing the conversation data.

            Returns:
                A dictionary indicating the success of the operation.
            """
            userDb = await UserDb.fromUserHash(ctx.userHash)
            await userDb.saveConversation(input)
            return { success: True }
        }),
        updateAll=procedure.input(ConversationSchemaArray).mutation(async ({ ctx, input }) => {
            """
            Updates multiple conversations.

            Args:
                ctx: The context object.
                input: The input object containing an array of conversation data.

            Returns:
                A dictionary indicating the success of the operation.
            """
            userDb = await UserDb.fromUserHash(ctx.userHash)
            await userDb.saveConversations(input)
            return { success: True }
        }),
    )
