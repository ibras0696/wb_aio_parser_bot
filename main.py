import asyncio
import logging
from contextlib import suppress

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramBadRequest

from config import BOT_TOKEN
from database import create_table
from handlers import router
from middleware import ErrorHandlerMiddleware


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Подключаем middleware ОДИН раз на все события
    dp.update.middleware(ErrorHandlerMiddleware())

    # Подключаем роутеры
    dp.include_router(router)

    # Очистка предыдущих обновлений
    with suppress(TelegramBadRequest):
        await bot.delete_webhook(drop_pending_updates=True)

    # Запуск
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    try:
        asyncio.run(create_table())
        asyncio.run(main())
    except TelegramBadRequest as e:
        logging.error(f"Telegram API error: {e}")
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
    except Exception as e:
        logging.critical(f"Unexpected error: {e}", exc_info=True)