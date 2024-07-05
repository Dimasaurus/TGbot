import asyncio
from aiogram.types import Message
from celery import Celery
from datetime import datetime, timedelta
from bot import bot

app = Celery('myapp', broker = 'amqp://guest:guest@localhost') #celery -A tasks worker --pool=gevent -l info

@app.task(name = 'handlers.handlers_basic.Notification_planned')
def Notification_planned(chat_id: int,time: datetime):
    
    asyncio.run(send_notification(chat_id,time))
    
    
    
async def send_notification(chat_id: int, time: datetime):   
   await bot.send_message(chat_id = chat_id, text = f"Вы просили написать вам в {time}")  
   
   