from aiogram import Router

from filters.admin import AdminFilter
from handlers.admin import admin, payments

admin_router = Router()
admin_router.message.filter(AdminFilter())

admin_router.include_routers(*[
    payments.router,  # Payment approval/rejection
    admin.router,
])
