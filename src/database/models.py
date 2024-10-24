from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class User(Base):
    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    fullname: Mapped[str]
    username: Mapped[str | None] = mapped_column(String(32))
    phone_number: Mapped[str | None] = mapped_column(String(20))

    def __str__(self):
        return f"User(id={self.id}, fullname={self.fullname}, telegram_id={self.telegram_id})"

    def __repr__(self):
        return self.__str__()


class Key(Base):
    __tablename__ = 'keys'
    __table_args__ = (UniqueConstraint('user_id', 'key'),)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    key: Mapped[str]
    expired_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    def __str__(self):
        return f"Key(id={self.id}, user_id={self.user_id}, key={self.key})"

    def __repr__(self):
        return self.__str__()
