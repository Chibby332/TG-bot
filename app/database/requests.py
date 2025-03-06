from app.database.models import async_session
from app.database.models import User, Info
from sqlalchemy import select
from sqlalchemy import BigInteger

async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id = tg_id))
            await session.commit() 

async def check_snils(snils):
    async with async_session() as session:
        snils = int(snils)
        result = await session.execute(
            select(Info.request_id, Info.request_name).where(Info.snils == snils)
        )
        
        requests = result.all()
        if not requests:
            return []
        else:
            return requests

async def check_id(id):
    async with async_session() as session:
        id = int(id)
        result = await session.execute(
            select(Info.request_name, Info.status, Info.money).where(Info.request_id == id)
        )
        
        request_info = result.fetchone()
        if not request_info:
            return None
        
        return {
            "request_name": request_info[0],
            "status": request_info[1],
            "money": request_info[2]
        }