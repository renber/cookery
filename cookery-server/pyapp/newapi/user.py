from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from starlette import status as httpstatus
from pydantic import BaseModel
import bcrypt
from pyapp.permissions import PermissionStr
from pyapp.session import sessionMgr, TokenStatus, getCurrentSession
from pyapp.dao.base import orm
from pyapp.dao.entities import User
from pyapp.dao.user import db_is_usr_active, db_usr_get, db_get_pwd, db_usr_get_permissions
from pyapp.fapi_auth import UserSession, valid_session

router = APIRouter(prefix='/user') # description="User account management & authorization"

class LoginCredentials(BaseModel):
    username: str
    password: str

class LoginResult(BaseModel):
    """
    The result of a successful login attempt
    """
    user: str
    displayName: str
    token: str


@orm.db_session
@router.post("/login", )
async def login(credentials: LoginCredentials) -> LoginResult:
    print("Received login request by user " + credentials.username)

    # check if user account exists and is active
    if not db_is_usr_active(credentials.username):
        print("User account does not exist / is disabled")
        raise HTTPException(httpstatus.HTTP_404_NOT_FOUND)

    # check username and password
    hashed_password = db_get_pwd(credentials.username)

    if not bcrypt.checkpw(credentials.password.encode('utf-8'), hashed_password):
        print('Wrong password')
        raise HTTPException(httpstatus.HTTP_401_UNAUTHORIZED)

    userinfo = db_usr_get(credentials.username)

    token = sessionMgr.newSession(userinfo.usr_email, userinfo.usr_uid)

    return LoginResult(user=userinfo.usr_email, displayName=userinfo.usr_name, token=token)


@router.get('/isloggedin')
async def is_logged_in(session: Annotated[UserSession, Depends(valid_session)]) -> bool:
    return True
