from fastapi. security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Annotated, Optional
from fastapi import Depends, HTTPException
from starlette import status as httpstatus

from pyapp.session import sessionMgr, TokenStatus

bearer_security = HTTPBearer(auto_error=True)


class UserSession:

    token = None
    userid = None

    def __init__(self, token: str, userid: str):
        self.token = token
        self.userid = userid


def valid_session(auth: Optional[HTTPAuthorizationCredentials] = Depends(bearer_security)) -> UserSession:

    if auth.scheme != 'Bearer':
        print("Unsupported authentication scheme: " + auth.scheme)
        raise HTTPException(status_code=httpstatus.HTTP_400_BAD_REQUEST)

    token = auth.credentials

    if not token or len(token) == 0:
        raise HTTPException(
            status_code=httpstatus.HTTP_401_UNAUTHORIZED,
            detail="Not authorized",
        )

    print("Received token " + token)

    # check if token is a session token
    token_state, userid = sessionMgr.getTokenStatus(token)
    if token_state == TokenStatus.SESSION_TOKEN_VALID:
        print("Authorized with VALID session token: " + token)
        return UserSession(token, userid)

    # token was neither a valid session nor api token
    print("Tried to authorize with INVALID or expired token: " + token)
    raise HTTPException(
        status_code=httpstatus.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
    )
