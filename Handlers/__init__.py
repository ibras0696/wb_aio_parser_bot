from aiogram import Router

# Пользовательские Роутеры
from .Users.Handlers.user_handlers import router as user_router
from .Users.Handlers.table_search_handler import router as table_search_router
from .Users.Handlers.search_default_handler import router as search_default_router

# Админские Роутеры
from .Admin.Handlers.admin_panel import router as admin_router
router = Router()

# Пользовательские
router.include_routers(
    user_router,
    table_search_router,
    search_default_router
)

# Админ
router.include_routers(
    admin_router,
)
