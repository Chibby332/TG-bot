import os
from dotenv import load_dotenv
from sqlalchemy import BigInteger,String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
load_dotenv()
engine = create_async_engine(url='postgresql+asyncpg://postgres:14112003a@localhost:5432/data')

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)

class Info(Base):
    __tablename__ = 'info'

    id: Mapped[int] = mapped_column(primary_key=True)
    snils = mapped_column(BigInteger)
    request_id = mapped_column(BigInteger)
    request_name: Mapped[str] = mapped_column(String(25))
    status: Mapped[str] = mapped_column(String(25))
    money = mapped_column(BigInteger)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
