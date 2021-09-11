from aiogram.dispatcher.filters.state import StatesGroup, State


class User(StatesGroup):
    MAIN_MENU = State()
    IS_ANONYMOUS = State()
    SEND_POST = State()
