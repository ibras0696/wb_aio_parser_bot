import asyncio
import logging
from contextlib import suppress

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramBadRequest

from config import BOT_TOKEN
from database import create_table
from handlers import router


async def main():
    """Основная функция инициализации и запуска бота"""
    bot = Bot(token=BOT_TOKEN)  # Добавлен parse_mode по умолчанию
    dp = Dispatcher()

    # Подключение роутера
    dp.include_router(router)

    # Очистка предыдущих обновлений
    with suppress(TelegramBadRequest):  # Более элегантная обработка исключения
        await bot.delete_webhook(drop_pending_updates=True)

    # Запуск бота
    await dp.start_polling(bot)


if __name__ == '__main__':
    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"  # Добавлен формат логов
    )

    try:
        # Инициализация БД и запуск бота
        asyncio.run(create_table())
        asyncio.run(main())
    except TelegramBadRequest as e:
        logging.error(f"Telegram API error: {e}")
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")  # Логирование вместо print
    except Exception as e:
        logging.critical(f"Unexpected error: {e}", exc_info=True)