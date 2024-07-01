from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from celery import Celery
from datetime import datetime, timedelta

app = Celery('myapp', broker = 'amqp://guest:guest@localhost') #celery -A handlers_basic worker --pool=eventlet -l info

app.conf.task_serializer = 'pickle'
app.conf.result_serializer = 'pickle'
app.conf.accept_content = ['application/json', 'application/x-python-serialize']

router = Router()

@app.task(name = 'handlers.handlers_basic.Notification_planned')
def Notification_planned(MessageData: dict):
    message = Message.model_validate(MessageData)
    message.reply(f"Вы просили написать вам в {datetime.now()}")


@router.message(Command("start"))
async def process_start_command(message: Message):
    await message.reply("Fired up and ready to serve")

@router.message(Command("help"))
async def process_help_command(message: Message):
    await message.reply("Пока это эхо бот! \n напиши что угодно и бот ответит")

@router.message(Command("setNot"))
async def process_setNot_command(message: Message):
    
    PlannedTime = datetime.now() + timedelta(seconds=20)
    PlannedTimeUTC = datetime.utcnow() + timedelta(seconds=20)
    
    await message.answer(f"Сообщение придет в {PlannedTime}")
    chatData = {'id': message.chat.id, 'type': message.chat.type}
    MessageData = {'user_id': message.from_user.id, 'full_name': message.from_user.full_name, 'username': message.from_user.username, 'message_id': message.message_id, 'date': message.date, 
    'chat': chatData}
    Notification_planned.apply_async(args = [MessageData],eta = PlannedTimeUTC)

@router.message()
async def echo_message(msg: Message):
    await msg.answer(msg.text)
    
  

