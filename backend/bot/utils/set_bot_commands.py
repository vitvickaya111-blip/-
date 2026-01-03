import logging
from gettext import gettext as _

from aiogram import Bot, exceptions
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats, BotCommandScopeChat


async def set_default_commands(bot: Bot):
    await bot.delete_my_commands()
    commands = [
        BotCommand(command="start", description="Главное меню"),
        BotCommand(command="help", description="Помощь и навигация"),
        BotCommand(command="channel", description="Подписаться на канал"),
        BotCommand(command="consultation", description="Записаться на консультацию"),
    ]
    return await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())


async def set_admin_commands(bot: Bot, admin_ids: list[int]):
    for admin_id in admin_ids:
        try:
            await bot.set_my_commands(
                [
                    BotCommand(command="start", description="Главное меню"),
                    BotCommand(command="help", description="Помощь и навигация"),
                    BotCommand(command="channel", description="Подписаться на канал"),
                    BotCommand(command="consultation", description="Записаться на консультацию"),
                    BotCommand(command="admin", description="Админ-панель"),
                    BotCommand(command="payments", description="Список ожидающих платежей"),
                    BotCommand(command="approve", description="Подтвердить платеж: /approve USER_ID"),
                    BotCommand(command="reject", description="Отклонить платеж: /reject USER_ID"),
                ], scope=BotCommandScopeChat(chat_id=admin_id)
            )
        except exceptions.TelegramBadRequest:
            logging.info(f"Can't set admin commands: chat {admin_id} not found.")
    return
