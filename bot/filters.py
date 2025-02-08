from aiogram.filters import BaseFilter
from aiogram.types import Message


class WhiteList(BaseFilter):
    async def __call__(self, message: Message, users_list) -> bool:
        print(users_list)
        return message.from_user.id in users_list
