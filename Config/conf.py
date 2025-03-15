import dotenv
import os


# Загрузка данных с .env
dotenv.load_dotenv()

# Получение Токена
bot_token = os.getenv('TOKEN')

ID_ADMIN = int(os.getenv('ID_ADMIN'))
