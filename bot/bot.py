import re

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import F

from .config import load_config


config = load_config()

bot_token = config.token
users_list = config.users_ids

bot = Bot(token=bot_token)
dp = Dispatcher()

@dp.message(CommandStart(), F.from_user.id.in_(users_list))
async def process_start_command(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}!\n"
                         f"Отправь мне IMEI, чтобы узнать детальную информацию об устройстве.")

@dp.message(CommandStart(), F.from_user.id.not_in(users_list))
async def process_start_command(message: Message):
    await message.answer("Нет доступа к боту, обратитесь к администратору.")

@dp.message(F.text.regexp(re.compile(r"^\d{15}$")))
async def process_imei(message: Message):
    pass

if __name__ == "__main__":
    dp.run_polling(bot)