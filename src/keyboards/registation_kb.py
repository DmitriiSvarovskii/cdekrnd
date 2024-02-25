from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from src.lexicons import register_new_user, cancel_registr_txt


async def create_kb_register_user():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(
            text=value['text'], callback_data=value['callback_data'])
        for value in register_new_user.values()
    ]

    keyboard.row(*buttons, width=1)

    return keyboard.as_markup()


def create_kb_register_manager():
    button = KeyboardButton(text=cancel_registr_txt['cancel_registration'])
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button]],
        resize_keyboard=True
    )
    return keyboard
