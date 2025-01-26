import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest
from sqlalchemy.orm import sessionmaker
from db.db import engine, SessionLocal
from models import User, Whitelist
from check import check_imei
import os
import dotenv
from db.db import Base, SessionLocal
dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO)

API_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

def create_user_if_not_exists(session, tg_id, name):
    """Создает пользователя в базе данных, если его нет"""
    user = session.query(User).filter_by(tg_id=tg_id).first()
    if not user:
        user = User(name=name, tg_id=tg_id)
        session.add(user)
        session.commit()
    return user

async def send_not_in_whitelist(message: Message):
    """Ответ пользователю, если его нет в whitelist"""
    await message.reply("Тебя нет в вайтлисте")

async def handle_check_imei(message: Message, imei: str):
    """Обрабатывает проверку IMEI"""
    try:
        props = check_imei(imei)['properties']
        result = "\n".join(f'"{key}": "{value}"' for key, value in props.items())
        await message.reply(f"Результаты проверки:\n{result}")
    except Exception as e:
        await message.reply(f"Ошибка при проверке IMEI: {e}")

@dp.message(Command(commands=['start', 'help']))
async def cmd_start(message: Message):
    await message.reply("Привет! Отправь IMEI для проверки.")
def is_user_in_whitelist(session, user):
    """Проверяет, находится ли пользователь в whitelist"""
    return user.is_in_whitelist(session)

def add_user_to_whitelist(session, user):
    """Добавляет пользователя в whitelist"""
    if not is_user_in_whitelist(session, user):
        whitelist_entry = Whitelist(user_id=user.id)
        session.add(whitelist_entry)
        session.commit()

@dp.message(Command(commands=['add_to_whitelist']))
async def cmd_add_to_whitelist(message: Message):
    tg_id = str(message.from_user.id)
    name = message.from_user.full_name

    with SessionLocal() as session:
        # Создание пользователя, если его нет
        user = create_user_if_not_exists(session, tg_id, name)

        # Добавление в whitelist
        add_user_to_whitelist(session, user)
        await message.reply("Ты был успешно добавлен в вайтлист!")
@dp.message()
async def message_handler(message: Message):
    tg_id = str(message.from_user.id)
    name = message.from_user.full_name

    with SessionLocal() as session:
        # Создание пользователя, если его нет
        user = create_user_if_not_exists(session, tg_id, name)

        # Проверка, есть ли пользователь в whitelist
        if not user.is_in_whitelist(session):
            await send_not_in_whitelist(message)
            return

        # Если пользователь в whitelist, проверяем IMEI
        imei = message.text.strip()
        if not imei.isdigit() or len(imei) not in [15, 16]:
            await message.reply("Пожалуйста, введите корректный IMEI (15-16 цифр).")
            return

        await handle_check_imei(message, imei)



if __name__ == "__main__":
    dp.run_polling(bot)
