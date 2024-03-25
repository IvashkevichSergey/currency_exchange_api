from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.models.users import User
from app.api.schemas.token import Token
from app.api.schemas.users import UserCreate, UserBase
from app.auth import generate_access_token, check_user_auth
from app.db.database import get_session
from app.utils.user_service import get_user_by_username, create_new_user, auth_user

auth_router = APIRouter(prefix="/auth")


@auth_router.post('/register/', status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    """Router for users sign up"""
    user = await get_user_by_username(session, user_data.username)
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail={"error": "Choose another username"})
    user = create_new_user(session, user_data)
    try:
        await session.commit()
        return f"User {user.username} has been added successfully"
    except IntegrityError:
        await session.rollback()
        return


# @auth_router.get('/users/{username}', response_model=UserBase)
# async def profile_user(username: str, session: AsyncSession = Depends(get_session)):
#     """Router for checking information about user"""
#     user = await get_user_by_username(session, username)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#                             detail="Invalid username")
#     return user


@auth_router.get('/profile/', response_model=UserBase)
def get_me(current_user: User = Depends(check_user_auth)):
    return current_user


@auth_router.post('/login/', response_model=Token)
async def login_user(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    user = await auth_user(session, **user_data.model_dump())
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid username or password")
    access_token = generate_access_token(user.username)
    return Token(access_token=access_token)

