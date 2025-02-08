import re
from datetime import datetime, timezone

from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import F
from aiogram import Router

from api_client import get_imei_info
from filters import WhiteList


router = Router()

@router.message(CommandStart(), WhiteList())
async def process_start_command(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}!\n"
                         f"Отправь мне IMEI, чтобы узнать детальную информацию об устройстве.")

@router.message(~WhiteList())
async def process_start_command(message: Message):
    await message.answer("Нет доступа к боту, обратитесь к администратору.")

@router.message(F.text.regexp(re.compile(r"^\d{15}$")), WhiteList())
async def process_imei(message: Message):
    imei = message.text

    try:
        response = await get_imei_info(imei)
        if type(response) == list:
            imei_info = response[0]
        else:
            imei_info = response
    except Exception as e:
        await message.answer(f"Проверка не удалась.\n"
                             f"Возникла ошибка: {e.__class__.__name__}"
                             f"Обратитесь к администратору.")
        
    status = imei_info.get("status")

    if status == None:
        status_message = imei_info.get("message")
        await message.answer(f"Проверка не удалась.\n"
                             f"Возникла ошибка: {status_message}")
    if status == "unsuccessful":
        await message.answer(f"IMEI {imei} не существует.")

    if status == "successful":
        data = imei_info.get("properties")
        await message.answer(
            f"IMEI: {imei}\n"
            f"Модель: {data.get("deviceName")}\n"
            f"Статус гарантии: {data.get("warrantyStatus")}\n"
            f"Страна продажи: {data.get("purchaseCountry")}\n"
            f"Дата продажи: {datetime.fromtimestamp(
                data.get("estPurchaseDate"), tz=timezone.utc
            ).strftime('%d.%m.%Y')}\n"
            f"Восстановлен: {'Да' if data.get("refurbished") else 'Нет'}\n"
        )

@router.message()
async def echo(message: Message):
    await message.answer(f"IMEI номер не распознан. Проверьте его и повторите попытку."
                         f"Номер должен состоять из 15 цифр."
                         f"Если ошибка повторится, обратитесь к администратору.")