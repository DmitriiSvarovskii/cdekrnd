from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.lexicons import manager_text
from src.utils import manager_utils


async def create_kb_support_man_main(
    user_id: int
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
