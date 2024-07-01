import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import handlers_basic
    
async def main():
    bot = Bot(token=TOKEN)
    disp = Dispatcher()
    
    disp.include_router(handlers_basic.router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await disp.start_polling(bot)

if __name__ == '__main__':  
    asyncio.run(main())