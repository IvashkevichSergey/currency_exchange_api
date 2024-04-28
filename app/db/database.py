from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.settings.config import settings
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(settings.async_database_url)
async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    """Base declarative class for DB models"""
    pass


async def get_session() -> AsyncSession:
    """Async session generator"""
    async with async_session_maker() as session:
        yield session
