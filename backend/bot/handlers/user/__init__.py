from aiogram import Router, F

from handlers.user import start, messages, quiz

user_router = Router()
user_router.message.filter(F.chat.func(lambda chat: chat.type == "private"))
user_router.include_routers(*[
    quiz.router,  # Quiz handlers (should be before start to handle quiz callbacks)
    start.router,
    messages.router,  # Should be last to catch all unhandled messages
])
