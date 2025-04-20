from aiogram.fsm.state import StatesGroup, State


# Состояние для отправки Текста
class AdminMassSendTextState(StatesGroup):
    text = State()


# Состояния для отправки Текста с Фото
class AdminMassSendTextAndPhotoState(StatesGroup):
    text = State()
    photo = State()


# Состояние для отправки Текста с Видео
class AdminMassSendTextAndVideoState(StatesGroup):
    text = State()
    video = State()


# Состояние для отправки Фото
class AdminMassSendPhotoState(StatesGroup):
    photo = State()


# Состояние для отправки Видео
class AdminMassSendVideoState(StatesGroup):
    video = State()

