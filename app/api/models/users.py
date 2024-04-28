from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class User(Base):
    """User DB model"""
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
