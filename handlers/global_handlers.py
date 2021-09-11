from view import messages, keyboards
from database import crud

from aiogram import types
from loader import dp
from utils.utils import error_except
from sqlalchemy.exc import IntegrityError
from states.states import User


@dp.message_handler(commands=["start"], state="*")
async def start(message: types.Message):
    """
    Пользователь отправил команду /start, переводим его в главное меню

    :param message: Объект сообщения
    """

    try:
        crud.create_user(user_id=message.from_user.id)
        await User.MAIN_MENU.set()
        await message.answer(messages.MAIN_MENU, reply_markup=keyboards.main_menu_kb)
    except IntegrityError:
        await User.MAIN_MENU.set()
        await message.answer(messages.MAIN_MENU, reply_markup=keyboards.main_menu_kb)
    except Exception as error:
        await error_except(message.from_user.id, error)
