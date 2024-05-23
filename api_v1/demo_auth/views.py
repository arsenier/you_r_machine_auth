import secrets
import uuid
from typing import Annotated, Any
from time import time

from fastapi import APIRouter, Depends, HTTPException, status, Header, Response, Cookie
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.users import crud
from core.models import db_helper
from .secret import get_hashed_password, check_hashed_password

router = APIRouter(tags=["Demo Auth"])

security = HTTPBasic()


async def get_auth_user_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> str:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"Authenticate": "Basic"},
    )
    user = await crud.get_user_by_username(
        session=session, username=credentials.username
    )
    print(user)
    if user is None:
        raise unauthed_exc

    hash = user.password_hash

    if not check_hashed_password(credentials.password, hash):
        print(credentials.password, hash)
        raise unauthed_exc

    # # secrets
    # if not secrets.compare_digest(
    #     credentials.password.encode("utf-8"),
    #     correct_password.encode("utf-8"),
    # ):
    #     raise unauthed_exc

    return credentials.username


@router.get("/basic-auth-username/", status_code=status.HTTP_200_OK)
def demo_basic_auth_username(
    auth_username: str = Depends(get_auth_user_username),
):
    return {
        "message": f"Hi, {auth_username}!",
        "username": auth_username,
    }


@router.get("/basic-auth/")
def demo_basic_auth_credentials(
    auth_username: str = Depends(get_auth_user_username),
):
    return {
        "username": auth_username,
        "active": True,
    }


@router.get("/token-introspection/")
def demo_basic_token_introspection(
    auth_username: str = Depends(get_auth_user_username),
):
    return {
        "username": auth_username,
        "active": True,
    }
