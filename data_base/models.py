from typing import Any
from sqlalchemy.orm import DeclarativeBase, Mapped, declarative_base, sessionmaker, mapped_column, MappedColumn
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import BigInteger, String, ForeignKey

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'Users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column()
    telegram_id: MappedColumn[Any] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(50))
    age: Mapped[int] = mapped_column(BigInteger)
    gender: Mapped[str] = mapped_column(String(15))
    search_gender: Mapped[str] = mapped_column(String(12))
    description: Mapped[str] = mapped_column(String(300))


async def async_main():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)