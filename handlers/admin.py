from aiogram import types

import config
from view import keyboards
from loader import dp, bot
from database import crud


@dp.callback_query_handler(text_contains="accept_", state="*")
async def accept_post(query: types.CallbackQuery):
    # Вдруг каким-то чудесным образом получится так, что сообщение с кнопками пришло не администратору
    if query.from_user.id != config.ADMIN_ID:
        return

    post = crud.get_post(post_id=int(query.data.split("_")[-1]))

    if post.post_status != config.PostStatuses.PENDING:
        return

    crud.edit_post_type(post_id=post.id, post_status=config.PostStatuses.ACCEPTED)

    caption = f"Сделал @{post.username}" if post.username else None
    if post.post_type == "photo":
        await bot.send_photo(chat_id=config.CHANNEL_ID, photo=post.file_id, caption=caption)
    else:
        await bot.send_video(chat_id=config.CHANNEL_ID, video=post.file_id, caption=caption)

    await bot.edit_message_reply_markup(
        chat_id=config.ADMIN_ID, reply_markup=keyboards.accepted_kb, message_id=query.message.message_id)


@dp.callback_query_handler(text_contains="deny_", state="*")
async def deny_post(query: types.CallbackQuery):
    # Вдруг каким-то чудесным образом получится так, что сообщение с кнопками пришло не администратору
    if query.from_user.id != config.ADMIN_ID:
        return

    post = crud.get_post(post_id=int(query.data.split("_")[-1]))

    if post.post_status != config.PostStatuses.PENDING:
        return

    crud.edit_post_type(post_id=post.id, post_status=config.PostStatuses.DENIED)
    await bot.edit_message_reply_markup(
        chat_id=config.ADMIN_ID, reply_markup=keyboards.denied_kb, message_id=query.message.message_id)
