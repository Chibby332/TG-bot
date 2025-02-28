import asyncio
from aiogram import Bot, Dispatcher

from app.handlers import router

async def main():
    bot = Bot(token='7804963067:AAGs6Nbo4j7hNOviNWU-hZx2l4ixjTnlFbI')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt():
        print('Бот выключен')  
    
