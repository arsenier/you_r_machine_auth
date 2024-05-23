from typing import TYPE_CHECKING, Annotated

from sqlalchemy import String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import Base


class User(Base):
    username: Mapped[str] = mapped_column(String(20), unique=True)
    password_hash: Mapped[str] = mapped_column()
