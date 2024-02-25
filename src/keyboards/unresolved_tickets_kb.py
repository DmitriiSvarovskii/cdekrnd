from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.lexicons import manager_text
from src.utils import manager_utils


async def create_kd_unresolved_tickets(
    user_id: int
):
    claims, wayllib = await manager_utils.get_unresolved_tickets_data(
        user_id=user_id
    )
    text = await manager_text.create_manager_unresolved_tickets_btn(
        claims=claims,
        wayllib=wayllib
    )
    keyboard = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(
            text=value['text'], callback_data=value['callback_data'])
        for value in text.values()
    ]

    keyboard.row(*buttons, width=1)
    keyboard.row(
        InlineKeyboardButton(
            text=manager_text.common_manager_text['main_menu'],
            callback_data='press_main_menu_manager'
        ), width=1
    )

    return keyboard.as_markup()
