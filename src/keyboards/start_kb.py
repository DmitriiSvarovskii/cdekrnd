from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from src.lexicons import manager_text, customer_text, registration_text
from src.utils import manager_utils


async def create_kb_register_user():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(
            text=value['text'], callback_data=value['callback_data'])
        for value in registration_text_new_user.values()
    ]

    keyboard.row(*buttons, width=1)

    return keyboard.as_markup()


def create_kb_register_manager():
    button = KeyboardButton(
        text=registration_text.cancel_registr_txt['cancel_registration'])
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button]],
        resize_keyboard=True
    )
    return keyboard


async def create_kb_client():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(
            text=value['text'], callback_data=value['callback_data'])
        for value in customer_text.main_client_dict.values()
    ]

    keyboard.row(*buttons, width=1)

    return keyboard.as_markup()


async def create_kb_support_man_main(
    user_id: int,
):
    data = await manager_utils.get_manager_data(user_id=user_id)
    main_text = await manager_text.create_manager_main_btn(
        data=data
    )
    keyboard = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(
            text=value['text'], callback_data=value['callback_data'])
        for value in main_text.values()
    ]

    keyboard.row(*buttons, width=1)

    return keyboard.as_markup()
