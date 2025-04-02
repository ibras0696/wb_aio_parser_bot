from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from wb_aio_parser_bot.Config import ID_ADMIN


class AdminTypeFilter(BaseFilter):
    def __init__(self, id_admin: int):
        self.id_admin = id_admin

    async def __call__(self, message: Message):
        return True if message.chat.id == ID_ADMIN else False


class AdminCallBackFilter(BaseFilter):
    def __init__(self, id_admin: int):
        self.id_admin = id_admin

    async def __call__(self, call_back: CallbackQuery):
        if not call_back.message:
            return False
        return call_back.message.chat.id == self.id_admin


is_admin_filter = AdminTypeFilter(ID_ADMIN)

call_is_admin_filter = AdminCallBackFilter(ID_ADMIN)