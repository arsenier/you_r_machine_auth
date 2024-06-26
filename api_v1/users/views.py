from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import crud
from .dependencies import user_by_id, user_by_username
from .schemas import UserSchema, UserCreate, UserUpdatePartial

router = APIRouter(tags=["Users"])


@router.get("/", response_model=list[UserSchema])
async def get_users(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_users(session=session)


@router.post(
    "/",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    if await crud.get_user_by_username(session, user_in.username) is None:
        return await crud.create_user(session=session, user_in=user_in)

    raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail=f"User {user_in.username} already exists!",
    )


@router.get("/{user_id}/", response_model=UserSchema)
async def get_user(
    user: UserSchema = Depends(user_by_id),
):
    return user


@router.patch(
    "/{user_id}/",
    response_model=UserSchema,
)
async def update_user_partial(
    user_update: UserUpdatePartial,
    user: UserSchema = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_user(
        session=session,
        user=user,
        user_update=user_update,
    )


@router.delete("/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user: UserSchema = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_user(session=session, user=user)
