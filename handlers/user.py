from aiogram import types

import config
from view import buttons, keyboards, messages
from loader import dp, bot
from states.states import User
from aiogram.dispatcher import FSMContext
from database import crud


@dp.message_handler(state=User.MAIN_MENU)
async def main_menu(message: types.Message):
    if message.text == buttons.new_post:
        await switch_to_post_status(message)
    else:
        await message.answer(text=messages.USE_ONLY_BUTTONS, reply_markup=keyboards.main_menu_kb)


async def switch_to_post_status(message: types.Message):
    """
    Спрашиваем у пользователя как он хочет отправить пост: анонимно или нет

    :param message: Объект сообщения Telegram
    """

    await User.IS_ANONYMOUS.set()
    await message.answer(text=messages.IS_POST_ANONYMOUS, reply_markup=keyboards.is_anonymous_kb)


@dp.message_handler(state=User.IS_ANONYMOUS)
async def is_anonymous_menu(message: types.Message, state: FSMContext):
    # Пользователь возвращается назад
    if message.text == buttons.back:
        await User.MAIN_MENU.set()
        await message.answer(messages.MAIN_MENU, reply_markup=keyboards.main_menu_kb)
        return

    if message.text in [buttons.yes, buttons.no]:
        is_anonymous = message.text == buttons.no

        async with state.proxy() as data:
            data["is_anonymous"] = is_anonymous

        await switch_to_sending_post(message)
    else:
        await message.answer(text=messages.USE_ONLY_BUTTONS, reply_markup=keyboards.is_anonymous_kb)


async def switch_to_sending_post(message: types.Message):
    """
    Переводит пользователя к отправке поста

    :param message: Объект сообщения Telegram
    """

    await User.SEND_POST.set()
    await message.answer(text=messages.SEND_POST, reply_markup=keyboards.back_kb)


@dp.message_handler(state=User.SEND_POST, content_types=[types.ContentType.TEXT])
async def send_post_menu(message: types.Message):
    if message.text == buttons.back:
        await switch_to_post_status(message)
        return
    else:
        await message.answer(text=messages.USE_ONLY_BUTTONS, reply_markup=keyboards.back_kb)


@dp.message_handler(state=User.SEND_POST, content_types=[types.ContentType.PHOTO, types.ContentType.VIDEO])
async def send_post(message: types.Message, state: FSMContext):
    if message.content_type == "photo":
        file_id = message.photo[0].file_id
    else:
        file_id = message.video.file_id

    async with state.proxy() as data:
        # Если пользователь хочет, чтобы его авторство было указано и при этом его юзернейм не пустой
        username = None
        if not data["is_anonymous"] and message.from_user.username:
            username = message.from_user.username

    # Сохраняем пост в базу данных
    post = crud.create_post(post_type=message.content_type, file_id=file_id, username=username)

    caption = f"Сделал @{username}" if username else None
    if message.content_type == "photo":
        await bot.send_photo(
            chat_id=config.ADMIN_ID, photo=file_id,
            caption=caption, reply_markup=keyboards.accept_or_deny_post(post.id))
    else:
        await bot.send_video(
            chat_id=config.ADMIN_ID, video=file_id,
            caption=caption, reply_markup=keyboards.accept_or_deny_post(post.id))

    await message.answer(text=messages.SENT_TO_ADMIN)
    await User.MAIN_MENU.set()
    await message.answer(messages.MAIN_MENU, reply_markup=keyboards.main_menu_kb)
