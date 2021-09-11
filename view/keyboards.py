from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from view import buttons

main_menu_kb = ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
main_menu_kb.add(KeyboardButton(buttons.new_post))

is_anonymous_kb = ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
is_anonymous_kb.row(KeyboardButton(buttons.yes), KeyboardButton(buttons.no))
is_anonymous_kb.add(KeyboardButton(buttons.back))

back_kb = ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
back_kb.add(KeyboardButton(buttons.back))


def accept_or_deny_post(post_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(buttons.accept, callback_data=f"accept_{post_id}"))
    kb.add(InlineKeyboardButton(buttons.deny, callback_data=f"deny_{post_id}"))
    return kb


accepted_kb = InlineKeyboardMarkup()
accepted_kb.add(InlineKeyboardButton(buttons.accepted, callback_data="accepted"))

denied_kb = InlineKeyboardMarkup()
denied_kb.add(InlineKeyboardButton(buttons.denied, callback_data="denied"))
