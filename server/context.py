from next_auth import getServerSession
from auth_utils import getUserHash
from auth_options import authOptions
from trpc_server import inferAsyncReturnType
from trpc_server.adapters.next import CreateNextContextOptions

async def createContext(opts: CreateNextContextOptions):
    """
    Create the TRPC context for Next.js serverless API routes.

    Args:
        opts (CreateNextContextOptions): Options for creating the context.

    Returns:
        dict: The TRPC context containing the request, response, session, and userHash.
    """
    session = await getServerSession(opts.req, opts.res, authOptions)
    userHash = None
    if session:
        userHash = await getUserHash(opts.req, opts.res)
    return {
        'req': opts.req,
        'res': opts.res,
        'session': session,
        'userHash': userHash
    }

Context = inferAsyncReturnType[typeof(createContext)]
