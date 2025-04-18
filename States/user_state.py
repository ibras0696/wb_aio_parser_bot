from aiogram.fsm.state import StatesGroup, State


class SearchStates(StatesGroup):
    search = State()
    total = State()
    sorting = State()
    limited = State()


class TableSearchStates(StatesGroup):
    search = State()
    total = State()
    sorting = State()
