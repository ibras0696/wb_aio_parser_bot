import dotenv
import os


# Загрузка данных с .env
dotenv.load_dotenv()
def get_id_admin():
    try:
        return int(os.getenv('ID_ADMIN'))
    except Exception:
        raise 'Не правильный ID админа или отсутствует'


def get_api_toke_bot():
    try:
        return os.getenv('TOKEN')
    except Exception:
        raise 'Отсутствует Токен или не правильный'



BOT_TOKEN = get_api_toke_bot()

# Получение Токена

ID_ADMIN = get_id_admin()
