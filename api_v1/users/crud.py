"""
Create
Read
Update
Delete
"""

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import User
from api_v1.demo_auth.secret import get_hashed_password

from .schemas import UserCreate, UserUpdatePartial


async def get_users(session: AsyncSession) -> list[User]:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    return await session.scalar(stmt)


async def create_user(session: AsyncSession, user_in: UserCreate) -> User:

    username = user_in.username
    password = user_in.password

    hash = get_hashed_password(password=password)

    user = User(username=username, password_hash=hash)
    session.add(user)
    await session.commit()
    # await session.refresh(user)
    return user


async def update_user(
    session: AsyncSession,
    user: User,
    user_update: UserUpdatePartial,
) -> User:
    hash = get_hashed_password(password=user_update.password)
    setattr(
        user,
        "password_hash",
        hash,
    )
    await session.commit()
    return user


async def delete_user(
    session: AsyncSession,
    user: User,
) -> None:
    await session.delete(user)
    await session.commit()
