from datetime import datetime
from uuid import UUID
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True
    __table_args__ = {'extend_existing': True}

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class User(Base):
    __tablename__ = 'users'

    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    fullname: Mapped[str]
    username: Mapped[str | None] = mapped_column(String(32))
    phone_number: Mapped[str | None] = mapped_column(String(20))
    expired_at: Mapped[datetime]

    def __str__(self):
        return f"User fullname={self.fullname}, telegram_id={self.tg_id})"

    def __repr__(self):
        return self.__str__()


class Link(Base):
    __tablename__ = 'links'
    __table_args__ = (UniqueConstraint('user_tg_id', 'url'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_marzban_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True))
    user_tg_id: Mapped[int] = mapped_column(ForeignKey('users.tg_id'))
    url: Mapped[str]

    def __str__(self):
        return f"Link(id={self.id}, user_id={self.user_tg_id}, link={self.url})"

    def __repr__(self):
        return self.__str__()
