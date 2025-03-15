from aiogram import Router

# Пользовательские Роутеры
from .Users.Handlers.user_handlers import router as user_router

# Админские Роутеры
from .Admin.Handlers.admin_panel import router as admin_router
router = Router()

# Пользовательские
router.include_routers(
    user_router,
)

# Админ
router.include_routers(
    admin_router,
)
