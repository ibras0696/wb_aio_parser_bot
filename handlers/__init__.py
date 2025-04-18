from aiogram import Router

# ✅ Абсолютные импорты (от корня проекта)
from wb_aio_parser_bot.handlers.users.user_handlers import router as user_router
from wb_aio_parser_bot.handlers.users.table_search_handler import router as table_search_router
from wb_aio_parser_bot.handlers.users.search_default_handler import router as search_default_router

from wb_aio_parser_bot.handlers.admin.admin_panel import router as admin_router
from wb_aio_parser_bot.handlers.admin.export_handler import router as export_admin_router
from wb_aio_parser_bot.handlers.admin.mass_send_message_handler import router as mass_send_message_router

router = Router()

# Пользовательские
router.include_router(user_router)
router.include_router(table_search_router)
router.include_router(search_default_router)

# Админ
router.include_router(admin_router)
router.include_router(export_admin_router)
router.include_router(mass_send_message_router)