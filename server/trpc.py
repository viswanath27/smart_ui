from trpc import TRPCError, initTRPC
from context import Context

# Create the t-object using the TRPC server initializer
t = initTRPC.context[Context].create()

def middleware(handler):
    """
    TRPC middleware that checks for user authorization.

    Args:
        handler (Callable): The middleware handler function.

    Returns:
        Any: The result of the middleware handler function.
    """
    async def secure(ctx, next):
        """
        Middleware function that checks if the user is authorized.

        Args:
            ctx (Context): The TRPC context.
            next (Callable): The next middleware function.

        Raises:
            TRPCError: If the user is unauthorized.

        Returns:
            Any: The result of the next middleware function.
        """
        if not ctx.userHash:
            raise TRPCError(code='UNAUTHORIZED')
        return await next({
            'ctx': {
                'userHash': ctx.userHash
            }
        })

    return secure(handler)

router = t.router
publicProcedure = t.procedure
procedure = t.procedure.use(middleware)
