from typing import Any, Union
from next import NextApiRequest, NextApiResponse
from next_auth import getServerSession
import crypto

def ensureHasValidSession(req: NextApiRequest, res: NextApiResponse) -> bool:
    """
    Ensures that the request has a valid session.

    Args:
        req (NextApiRequest): The Next.js API request object.
        res (NextApiResponse): The Next.js API response object.

    Returns:
        bool: True if the session is valid, False otherwise.

    """
    session = await getServerSession(req, res, authOptions)
    return session is not None

def getUserHash(req: NextApiRequest, res: NextApiResponse) -> str:
    """
    Retrieves the user hash from the provided request.

    Args:
        req (NextApiRequest): The Next.js API request object.
        res (NextApiResponse): The Next.js API response object.

    Returns:
        str: The user hash.

    Raises:
        Error: If the user is unauthorized or no email is found in the session.

    """
    session = await getServerSession(req, res, authOptions)
    if not session:
        raise Error('Unauthorized')
    email = session.user.email
    if not email:
        raise Error('Unauthorized. No email found in session')
    return getUserHashFromMail(email)

def getUserHashFromMail(email: str) -> str:
    """
    Generates a hash based on the provided email.

    Args:
        email (str): The email to generate the hash from.

    Returns:
        str: The generated hash.

    """
    hash = crypto.createHash('sha256').update(email.encode('utf-8')).hexdigest()
    return hash

