from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.settings.config import settings
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(settings.async_database_url)
async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession)


class Base(DeclarativeBase):
    pass


async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
