import asyncio
from aiogram.types import Message,  URLInputFile
from aiogram.filters import Command
from celery import Celery
from datetime import datetime, timedelta
from tasks import Notification_planned
from bot import disp, bot
import psycopg2
from config import URL

DatabaseURL = URL

@disp.message(Command("start"))
async def process_start_command(message: Message):
    await message.reply("Fired up and ready to serve")

@disp.message(Command("help"))
async def process_help_command(message: Message):
    await message.reply("Пока это эхо бот! \n напиши что угодно и бот ответит")

@disp.message(Command("setNot"))
async def process_setNot_command(message: Message):
    
    PlannedTime = datetime.now() + timedelta(seconds=20)
    PlannedTimeUTC = datetime.utcnow() + timedelta(seconds=20)
    await message.answer(f"Сообщение придет в {PlannedTime}")
    Chat_id = message.chat.id
    Notification_planned.apply_async(args = [Chat_id,PlannedTime],eta = PlannedTimeUTC)

@disp.message(Command("getPost"))
async def getPost(msg: Message):
    conn = psycopg2.connect(DatabaseURL)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM post_contents ORDER BY post_id DESC LIMIT 1")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    await msg.answer(text = f"{result}")

@disp.message()
async def echo_message(msg: Message):
    image_from_url = URLInputFile("https://cdn.download.ams.birds.cornell.edu/api/v1/asset/414766991/900")
    result = await msg.answer_photo(
        image_from_url,
        caption=msg.text
    )


async def main():  
    await bot.delete_webhook(drop_pending_updates=True)
    await disp.start_polling(bot)

if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
    
  

