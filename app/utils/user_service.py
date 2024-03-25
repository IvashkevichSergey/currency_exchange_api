from typing import Optional

from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.models.users import User
from app.api.schemas.users import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"])


async def get_user_by_username(session: AsyncSession, username: str) -> User:
    """Return a User instance by username from DB"""
    query = select(User).where(User.username == username)
    result = await session.execute(query)
    return result.scalar()


def create_new_user(session: AsyncSession, user_data: UserCreate) -> User:
    """Create an instance of new User"""
    user_password = pwd_context.hash(user_data.password)
    new_user = User(username=user_data.username, password=user_password)
    session.add(new_user)
    return new_user


async def auth_user(session: AsyncSession, username: str, password: str) -> Optional[User]:
    """Check if the user exists and the password is correct"""
    user = await get_user_by_username(session, username)
    if not (user and pwd_context.verify(password, user.password)):
        return None
    return user

