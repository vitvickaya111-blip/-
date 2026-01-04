from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from typing import Union

from settings.app_settings import AppSettings


class AdminFilter(BaseFilter):
    is_admin: bool = True

    async def __call__(self, obj: Union[Message, CallbackQuery], settings: AppSettings) -> bool:
        return (obj.from_user.id in settings.bot.admin_ids) == self.is_admin
